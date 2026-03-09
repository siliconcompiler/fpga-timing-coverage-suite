/*
Circuit Name: hamming_distance
SDC Name: set_output_delay
Description: 
    -Calculates the hamming distance between data_in and a fixed bit pattern.
    -This circuit has input and output registers, using 'set_output_delay' to the data output port
     will guide the logic elements toward the FPGA peripherals during PnR. 
    -Adjusting the delay value will affect setup time requirements and slack. 
*/

// Top module
module hamming_distance(
    input clk,
    input n_rst,
    input [7:0] data_in,
    output [3:0] data_out
);
    reg [7:0] input_reg;
    reg [3:0] output_reg;
    wire [7:0] xor_result;

    // Input/Output Registers
    always @(posedge clk or negedge n_rst) begin
        if (!n_rst) begin
            input_reg <= 8'b0;
            output_reg <= 4'b0;   
        end
        else begin
            input_reg <= data_in;
            output_reg <= count;
        end
    end

    // XOR
    assign xor_result = input_reg ^ 8'hF0; 

    // Population Count (combinational)
    integer i;
    reg [3:0] count;
    always @(*) begin
        count = 0;
        for (i = 0; i < 8; i = i + 1) begin
            count = count + xor_result[i];
        end
    end

    assign data_out = output_reg;

endmodule