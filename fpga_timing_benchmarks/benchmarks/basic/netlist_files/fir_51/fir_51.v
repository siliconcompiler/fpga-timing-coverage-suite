/* 
Transposed 51-tap FIR filter 

*/
module fir_51 (
    input wire clk,
    input wire rst_n,
    input wire signed [15:0] data_in,
    output reg signed [37:0] data_out
);
    //Coefficient ROM
    reg signed [15:0] coeff [0:50];

    always @(negedge rst_n) begin
        coeff[0] <= 16'd0; 
        coeff[1] <= 16'd1; 
        coeff[2] <= 16'd2; 
        coeff[3] <= 16'd3; 
        coeff[4] <= 16'd4; 
        coeff[5] <= 16'd5; 
        coeff[6] <= 16'd6; 
        coeff[7] <= 16'd7; 
        coeff[8] <= 16'd8; 
        coeff[9] <= 16'd9; 
        coeff[10] <= 16'd10; 
        coeff[11] <= 16'd11; 
        coeff[12] <= 16'd12; 
        coeff[13] <= 16'd13; 
        coeff[14] <= 16'd14; 
        coeff[15] <= 16'd15; 
        coeff[16] <= 16'd16; 
        coeff[17] <= 16'd17; 
        coeff[18] <= 16'd18; 
        coeff[19] <= 16'd19; 
        coeff[20] <= 16'd20; 
        coeff[21] <= 16'd21; 
        coeff[22] <= 16'd22; 
        coeff[23] <= 16'd23; 
        coeff[24] <= 16'd24; 
        coeff[25] <= 16'd25; 
        coeff[26] <= 16'd24; 
        coeff[27] <= 16'd23; 
        coeff[28] <= 16'd22; 
        coeff[29] <= 16'd21; 
        coeff[30] <= 16'd20; 
        coeff[31] <= 16'd19; 
        coeff[32] <= 16'd18; 
        coeff[33] <= 16'd17; 
        coeff[34] <= 16'd16; 
        coeff[35] <= 16'd15; 
        coeff[36] <= 16'd14; 
        coeff[37] <= 16'd13; 
        coeff[38] <= 16'd12; 
        coeff[39] <= 16'd11; 
        coeff[40] <= 16'd10; 
        coeff[41] <= 16'd9; 
        coeff[42] <= 16'd8; 
        coeff[43] <= 16'd7; 
        coeff[44] <= 16'd6; 
        coeff[45] <= 16'd5; 
        coeff[46] <= 16'd4; 
        coeff[47] <= 16'd3; 
        coeff[48] <= 16'd2; 
        coeff[49] <= 16'd1; 
        coeff[50] <= 16'd0;
    end

    //Systolic FIR Logic
    integer i;
    reg signed [37:0] sum [0:50];

    always @(posedge clk or negedge rst_n) begin
        if(!rst_n) begin 
            for(i = 0; i < 51; i = i + 1) begin
                sum[i] <= 38'b0;
            end
            data_out <= 16'b0;
        end
        else begin
            sum[0] <= data_in * coeff[0];
            for(i = 1; i < 51; i = i + 1) begin
                sum[i] <= (data_in * coeff[i]) + sum[i-1];
            end
            data_out <= sum[50];
        end
    end

endmodule
