/*
Circuit Name: multibit_rca
SDC Name: set_false_path
Description: 
    -This circuit has two independent adders with different bit widths.
    -Tell the STA tool to ignore the timing path of the longer adder by using 'set_false_path'.
    -Fmax should depend on the shorter adder when 'set_false_path' is used.
*/
// Top module
module multibit_rca #(parameter WIDTH_I = 128, WIDTH_II = 32)(
    input clk,
    input  [WIDTH_I-1:0] a_i,
    input  [WIDTH_I-1:0] b_i,
    input  [WIDTH_II-1:0] a_ii,
    input  [WIDTH_II-1:0] b_ii,
    output reg [WIDTH_I-1:0] y_i,
    output reg [WIDTH_II-1:0] y_ii
);
    // Wire and reg for adder I (WIDTH_I)
    wire [WIDTH_I-1:0] sum_i;
    reg [WIDTH_I-1:0] reg_a_i, reg_b_i;

    // Wire and reg for adder II (WIDTH_II)
    wire [WIDTH_II-1:0] sum_ii;
    reg [WIDTH_II-1:0] reg_a_ii, reg_b_ii;

    // Input and output are both registered
    always @(posedge clk) begin
        reg_a_i <= a_i;
        reg_b_i <= b_i;
        reg_a_ii <= a_ii;
        reg_b_ii <= b_ii;
        y_i <= sum_i;
        y_ii <= sum_ii;
    end

    ripple_adder #(.WIDTH(WIDTH_I)) rca_i(
        .a(reg_a_i),
        .b(reg_b_i),
        .sum(sum_i)
    );

    ripple_adder #(.WIDTH(WIDTH_II))rca_ii(
        .a(reg_a_ii),
        .b(reg_b_ii),
        .sum(sum_ii)
    );

endmodule

// 1-bit FA module
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

// Parameterized adder
// Final carry is discarded for simplicity
module ripple_adder #(parameter WIDTH = 128)(
    input  [WIDTH-1:0] a,
    input  [WIDTH-1:0] b,
    output [WIDTH-1:0] sum
);
    wire [WIDTH:0] carry;
    assign carry[0] = 1'b0;   // initial carry-in

    genvar i;
    generate
        for (i = 0; i < WIDTH; i = i + 1) begin : rca
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