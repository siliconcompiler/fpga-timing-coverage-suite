/*
A hardend implementation of vector-matrix multiplication
One 1x16 vector is multiplied with 16x2 matrix
Each column of the matrix is broadcasted one by one
*/

module vec_mul_pipe(
    input clk,
    input [15:0] vec,
    input [15:0] col,
    input sel,
    output [4:0] out1,
    output [4:0] out2
);
    reg [16:0] stage1; //each stage register has one select bit
    reg [5:0] stage2;
    wire [4:0] mul_result;
    wire en1, en2;

    vec_mul_unit VM1(
        .vec1(vec),
        .vec2(stage1[15:0]),
        .vec_out(mul_result)
    );

    decoder DE(
        .in(stage2[5]),
        .out1(en1),
        .out2(en2)
    );

    dff FF1( 
        .clk(clk),
        .en(en1),
        .D(stage2[4:0]),
        .Q(out1)
    );

    dff FF2( 
        .clk(clk),
        .en(en2),
        .D(stage2[4:0]),
        .Q(out2)
    );

    always @(posedge clk) begin
      stage1[15:0] <= col;
      stage[16] <= sel;

      stage2[4:0] <= mul_result;
      stage2[5] <= stage1[16];
    end


endmodule

module vec_mul_unit(
    input [15:0] vec1,
    input [15:0] vec2,
    output [4:0] vec_out
);
    wire [15:0] vec_mul;
    assign vec_mul = vec1 & vec2;

    assign vec_out = vec_mul[0] + vec_mul[1] + vec_mul[2] + vec_mul[3] + vec_mul[4] + 
    vec_mul[5] + vec_mul[6] + vec_mul[7] + vec_mul[8] + vec_mul[9] + vec_mul[10] + vec_mul[11] +
    vec_mul[12] + vec_mul[13] + vec_mul[14] + vec_mul[15];

endmodule 

module decoder(
    input in,
    output out1,
    output out2
);
    assign out1 = ~in;
    assign out2 = in;
endmodule

module dff(
    input clk,
    input en,
    input [4:0] D,
    output [4:0] Q
);
    always @(posedge clk) begin
        if (en) Q <= D;
        else Q <= Q;
    end
endmodule

/*
example SDCs

create_clock -name clk [get_ports clk]
set_clock_uncertainty 

//Set a loose clock period, adding set_clock_uncertainty will shrink the slack. 
*/