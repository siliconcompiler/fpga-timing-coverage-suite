/*
https://vlsitutorials.com/constraining-multi-cycle-path-in-synthesis/https://vlsitutorials.com/constraining-multi-cycle-path-in-synthesis/

allow multi cycles for 128-bit RCA
See how Fmax changes with varying multicycles allowed for it
*/

module long_critical_path_top (
    input clk,
    input  [127:0] a_128,
    input  [127:0] b_128,
    input  [31:0] a_32,
    input  [31:0] b_32;
    output [127:0] y_128;
    output [31:0] y_32;
);
    wire [127:0] sum_128;
    reg [127:0] reg_a_128, reg_b_128, y_128;

    wire [31:0] sum_32;
    reg [31:0] reg_a_32, reg_b_32, y_32;

    always @(posedge clk) begin
        reg_a_128 <= a_128;
        reg_b_128 <= b_128;
        reg_a_32 <= a_32;
        reg_b_32 <= b_32;
        y_128 <= sum_128;
        y_32 <= sum_32;
    end

    ripple_adder_128 rca_128(
        .a(reg_a_128),
        .b(reg_b_128),
        .sum(sum_128)
    );

    ripple_adder_32 rca_32(
        .a(reg_a_32),
        .b(reg_b_32),
        .sum(sum_32)
    );

endmodule

module dff_128(
    input wire clk,
    input wire [127:0] d, 
    output reg [127:0] q
);
    always @(posedge clk) begin
        q <= d;
    end
endmodule

module full_adder(
    input wire a,
    input wire b,
    input wire cin,
    output wire sum,
    output wire cout
);
    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));
endmodule

module ripple_adder_128 (
    input  [127:0] a,
    input  [127:0] b,
    output [127:0] sum
);
    (* keep *) wire [128:0] carry; //keep attribute 
    assign carry[0] = 1'b0;   // initial carry-in

    genvar i;
    generate
        for (i = 0; i < 128; i = i + 1) begin : rca
            full_adder fa (
                .a   (a[i]),
                .b   (b[i]),
                .cin (carry[i]),
                .sum (sum[i]),
                .cout(carry[i+1])
            );
        end
    endgenerate
endmodule

module ripple_adder_32(
    input [31:0] a,
    input [31:0] b,
    output [31:0] sum
);
    assign sum = a + b;
endmodule