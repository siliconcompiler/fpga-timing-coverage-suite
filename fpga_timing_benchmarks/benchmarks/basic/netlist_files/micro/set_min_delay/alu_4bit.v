/*
Circuit Name: alu_4bit
SDC Name: set_min_delay
Description: 
    -A simple 4-bit registered ALU that supports four arithmetic operations.
    -Assume an environment with a high clock latency or clock skew. This should be modeled with 'set_clock_latency'. 
     Such environment can increase the risk of hold violations with short pipelined circuits like this.
    -Using 'set_min_delay' between the two pipeline stages should allow this circuit to meet the hold requirement. 

SDC Example:
    create_clock -period 10.0 [get_ports clk]

    set_clock_latency 0.0 [get_pins {reg_a[*]/clk reg_b[*]/clk reg_op[*]/clk}]
    set_clock_latency 2.0 [get_pins {result_reg[*]/clk}]

    set_min_delay 2.5 -from [get_pins {reg_a[*]/Q reg_b[*]/Q reg_op[*]/Q}] -to [get_pins {result_reg[*]/D}]
*/

module alu_4bit(
    input clk,
    input [3:0] a, b,
    input [1:0] op,
    output [3:0] result
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