module clk_dvdr_top(
    input wire          clk,
    input wire [63:0]   a, 
    input wire [63:0]   b, 
    input wire          cin,
    output reg [63:0]   clk_sum,
    output reg [63:0]   gen_clk_sum
);
    wire [63:0] sum1, sum2;
    wire cout1, cout2;
    wire gen_clk;
    reg [63:0] reg_a, reg_b;
    reg [63:0] reg_a_gen, reg_b_gen;

    //Clock divider - gen_clock is half the frequency of clk
    clk_dvdr divider(.clk(clk), .gen_clk(gen_clk));

    //Two 64-bit ripple carry adders timed by clk and gen_clk
    rca_64 adder1(
        .a(reg_a), 
        .b(reg_b), 
        .cin(cin), 
        .sum(sum1), 
        .cout(cout1)
        );

    rca_64 adder2(
        .a(reg_a_gen), 
        .b(reg_b_gen), 
        .cin(cin), 
        .sum(sum2), 
        .cout(cout2)
        );

    //Two clock domains
    always @(posedge clk) begin
        clk_sum <= sum1;
        reg_a <= a;
        reg_b <= b;
    end

    always @(posedge gen_clk) begin
        gen_clk_sum <= sum2;
        reg_a_gen <= a;
        reg_b_gen <= b;
    end

endmodule 

//Clock divider module
module clk_dvdr(
    input wire clk,
    output wire gen_clk
);
    reg q;

    always @(posedge clk) begin
        q <= ~q;
    end

    assign gen_clk = q;
endmodule


//64-bit Adder and full adder modules
module rca_64(
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
        for(i = 0; i < 63; i = i + 1) begin : rca
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