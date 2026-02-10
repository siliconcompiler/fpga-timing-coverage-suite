/*
Circuit Name: rca_64
SDC Name: create_clock
Description: 
    -A 64-bit ripple carry adder with registers for inputs and outputs
    -STA should reflect the clock period specified by 'create_clock' by optimizing 
     placement and routing to reduce the critical path or reporting timing violations 
     if it cannot be met (CPD on k6_frac_N10_frac_chain_mem32K architecture is 11.1512ns)
*/

// Top module
module rca_64(
    input           clk,
    input [63:0]    a,
    input [63:0]    b,
    input           cin,
    output [63:0]   sum,
    output          cout
);
    // Register and wire definitions
    reg [63:0] reg_a, reg_b;
    reg [63:0] reg_sum;
    reg reg_cin, reg_cout;
    wire [63:0] wire_sum;
    wire wire_cout;

    // Ripple carry adder instance
    adder_64bit u_rca_64(
        .a(reg_a),
        .b(reg_b),
        .cin(reg_cin),
        .sum(wire_sum),
        .cout(wire_cout)
    );

    // Input and output registers 
    always @(posedge clk) begin
        reg_a <= a;
        reg_b <= b;
        reg_cin <= cin;
        reg_sum <= wire_sum;
        reg_cout <= wire_cout;
    end
    
    // Output assignment
    assign sum = reg_sum;
    assign cout = reg_cout;
endmodule

// 64-bit adder module
module adder_64bit(
    input [63:0]    a,
    input [63:0]    b,
    input           cin,
    output [63:0]   sum,
    output          cout
);

    wire [64:0] carry;
    assign carry[0] = cin;

    genvar i;
    generate
        for(i = 0; i < 64; i = i + 1) begin : rca
            fa u_fa(
                .a   (a[i]), 
                .b   (b[i]), 
                .cin (carry[i]), 
                .sum (sum[i]), 
                .cout(carry[i+1])
                );
        end
    endgenerate

    assign cout = carry[64];

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