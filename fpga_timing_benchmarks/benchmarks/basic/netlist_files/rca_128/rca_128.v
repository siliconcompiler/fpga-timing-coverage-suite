module long_critical_path_top (
    input clk,
    input  [127:0] a,
    input  [127:0] b,
    output reg [127:0] y
);
    wire [127:0] sum;

    ripple_adder_128 rca (
        .a(a),
        .b(b),
        .sum(sum)
    );

    always @(posedge clk) begin
        y <= sum;
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