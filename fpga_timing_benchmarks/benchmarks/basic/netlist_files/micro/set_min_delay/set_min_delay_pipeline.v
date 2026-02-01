/*
set_min_delay

very short pipeline with high clock latency (and possibly long clock cycle?)

A simple pipelined ALU
if we use high clock latency, alu result might reach the second pipeline stage too fast. So add min_delay to meet hold requirement 
*/

module alu_4bit(
    input clk,
    input [3:0] a, b,
    input [1:0] op,
    output [3:0] result,
);
    reg [3:0] reg_a, reg_b;
    reg [1:0] reg_op;

    always @(posedge clk) begin
        reg_a <= a;
        reg_b <= b;
        reg_op <= op;        
    end

    always @(posedge clk) begin
        case (reg_op)
            2'b00: result <= reg_a + reg_b; 
            2'b01: result <= reg_a - reg_b;
            2'b10: result <= reg_a & reg_b;
            2'b11: result <= reg_a | reg_b;
            default: result <= 4'b0;
        endcase
    end
endmodule 