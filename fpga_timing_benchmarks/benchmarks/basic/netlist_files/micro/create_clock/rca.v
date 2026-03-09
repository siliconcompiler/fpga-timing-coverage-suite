/*
Circuit Name: rca
SDC Name: create_clock
Description: 
    -A parameterized ripple carry adder with registers for inputs and outputs
    -STA should reflect the clock period specified by 'create_clock' by optimizing 
     placement and routing to reduce the critical path or reporting timing violations 
     if it cannot be met
*/

// Top module
module rca #(parameter WIDTH = 64)(
    input           clk,
    input [WIDTH-1:0]    a,
    input [WIDTH-1:0]    b,
    input           cin,
    output [WIDTH-1:0]   sum,
    output          cout
);
    // Registers for pipelining
    reg [WIDTH-1:0] reg_a, reg_b;
    reg [WIDTH-1:0] reg_sum;
    reg reg_cin, reg_cout;

    // Wire declaration
    wire [WIDTH-1:0] wire_sum;
    wire [WIDTH:0] carry;

    assign carry[0] = reg_cin;

    // Full adder instantiation
    genvar i;
    generate
        for(i = 0; i < WIDTH; i = i + 1) begin : rca
            fa u_fa(
                .a   (reg_a[i]), 
                .b   (reg_b[i]), 
                .cin (carry[i]), 
                .sum (wire_sum[i]), 
                .cout(carry[i+1])
                );
        end
    endgenerate

    // Input and output registers 
    always @(posedge clk) begin
        reg_a <= a;
        reg_b <= b;
        reg_cin <= cin;
        reg_sum <= wire_sum;
        reg_cout <= carry[WIDTH];
    end
    
    // Output assignment
    assign sum = reg_sum;
    assign cout = reg_cout;
endmodule

// 1-bit full adder module
module fa(
    input a,
    input b,
    input cin,
    output sum,
    output cout
);
    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));
endmodule