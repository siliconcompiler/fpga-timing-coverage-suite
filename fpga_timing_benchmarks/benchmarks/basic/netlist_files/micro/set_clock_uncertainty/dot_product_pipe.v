/*
Circuit Name: dot_product_pipe
SDC Name: set_clock_uncertainty
Description: 
    -This circuit multiplies a 1x16 vector with each column of a 16xN matrix (0 < N < 32)
    -Each column of the matrix is broadcast one by one by an external unit
    -There are two states for the control state machine - IDLE and COMPUTE
    -Set a loose clock period and constrain the circuit with 'set_clock_uncertainty'
     to see how slack is affected by the uncertainty value
*/

// Top module
module dot_product_pipe(
    input clk,
    input n_rst,
    input start, // Changes the control state to 'COMPUTE'
    input [4:0] num_col, // Number of columns of the matrix
    input [15:0] vec,
    input [15:0] col,
    output valid, // Valid flag for the output
    output mul_done, // Indicates if all columns have been computed
    output [4:0] out
);
    // Wires
    wire [4:0] scalar_out;
    wire in_valid, done;

    // Vector multiplier unit
    vector_multiplier u_vec_mul(
        .vec(vec_in_reg),
        .col(col_in_reg),
        .out(scalar_out)
    );

    // Control FSM
    control u_ctrl(
        .clk(clk),
        .n_rst(n_rst),
        .start(start),
        .num_col(num_col),
        .in_valid(in_valid),
        .done(done)        
    );

    // Pipeline Stage 1: Input is registered
    reg [15:0] vec_in_reg, col_in_reg;
    reg valid_stage1, done_stage1; 
    
    always @(posedge clk or negedge n_rst) begin
        if (!n_rst) begin
            vec_in_reg <= 0;
            col_in_reg <= 0;
            valid_stage1 <= 0;
            done_stage1 <= 0;
        end
        else begin
            vec_in_reg <= vec;
            col_in_reg <= col;
            valid_stage1 <= in_valid;
            done_stage1 <= done;
        end
    end

    // Pipeline Stage 2: Output is registered
    reg [4:0] scalar_out_reg;
    reg valid_stage2, done_stage2;

    always @(posedge clk or negedge n_rst) begin
        if (!n_rst) begin
            scalar_out_reg <= 0;
            valid_stage2 <= 0;
            done_stage2 <= 0;
        end
        else begin
            scalar_out_reg <= scalar_out;
            valid_stage2 <= valid_stage1;
            done_stage2 <= done_stage1;
        end
    end

    assign valid = valid_stage2;
    assign mul_done = done_stage2;
    assign out = scalar_out_reg;

endmodule

// Vector multiplier 
module vector_multiplier(
    input [15:0] vec,
    input [15:0] col,
    output [4:0] out
);
    wire [15:0] element_product;

    // Element-wise AND operation of two vectors
    assign element_product = vec & col; 

    // Accumulation of all element-wise products
    assign out = element_product[0] + element_product[1] + element_product[2] + element_product[3] +
            element_product[4] + element_product[5] + element_product[6] + element_product[7] +
            element_product[8] + element_product[9] + element_product[10] + element_product[11] +
            element_product[12] + element_product[13] + element_product[14] + element_product[15];
endmodule

// Control FSM
module control(
    input clk,
    input n_rst,
    input start,
    input [4:0] num_col,
    output reg in_valid,
    output reg done
);
    // State parameter definition
    parameter IDLE = 1'b0;
    parameter COMPUTE = 1'b1;

    // State registers
    reg curr_state, next_state;

    // Counter register
    reg [4:0] counter; 

    // State transition
    always @(posedge clk or negedge n_rst) begin
        if (!n_rst) begin
            curr_state <= IDLE;
        end
        else begin
            curr_state <= next_state;
        end
    end

    // Next state logic
    always @(*) begin
        case (curr_state)
            IDLE: begin
                if (start) next_state = COMPUTE;
                else next_state = IDLE;
            end
            COMPUTE: begin
                if (counter == num_col - 1) next_state = IDLE;
                else next_state = COMPUTE;
            end
            default: next_state = IDLE;
        endcase
    end

    // Output logic
    always @(posedge clk or negedge n_rst) begin
        if (!n_rst) begin
            counter <= 0;
            in_valid <= 0;
            done <= 0;
        end
        else begin
            case (next_state)
                IDLE: begin
                    counter <= 0;
                    in_valid <= 0;
                    done <= 0;
                end
                COMPUTE: begin
                    counter <= counter + 1;
                    in_valid <= 1;
                    done <= (counter == num_col - 1) ? 1 : 0;
                end
            endcase
        end
    end
endmodule