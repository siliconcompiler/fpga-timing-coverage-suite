/*
We should probably add set_clock_latency to the generated clocks to model path delay.


SDC example
create_clock clk0
create_clock clk1

create_generated_clock -name clk0mux -divide_by 1 -source [get_pins mux/in0] [get_pins mux/out]
create_generated_clock -name clk1mux -divide_by 1 -add (-master_clock clk1) -source [get_pins mux/in1] [get_pins mux/out]

//Telling the tool not to analyze the path between clk0 and clk1
set_clock_groups -logically_exclusive -group clk0 -group clk1 

//There simply exists no timing path between clk0mux and clk1mux 
set_clock_groups -physically exclusive -group clk0mux -group clk1mux
*/

module mul_clk(
    input clk0,
    input clk1,
    input sel,
    input a,
    input b,
    output comb1, 
    output fdm1_out
);
    wire clk_mux;
    wire fd0_out, fd1_out, fdm0_out, fdm1_out;
    wire comb1;
    wire [3:0] comb2;

    dff FD0(
        .clk(clk0),
        .D(a),
        .Q(fd0_out)
    );

    dff FD1(
        .clk(clk1),
        .D(a),
        .Q(fd1_out)
    );

    dff FDM0(
        .clk(clk_mux),
        .D(a),
        .Q(fdm0_out)
    );

    dff FDM1(
        .clk(clk_mux),
        .D(comb2[0]),
        .Q(fdm1_out)
    );
    
    mux_2to1 clock_mux(
        .in0(clk0),
        .in1(clk1),
        .sel(sel),
        .out(clk_mux)
    );

    //Combinational logic 
    //combine (fd0, fd1) and (fd1, fdm0).
    //The combination above drives some other register that's not fdm1
    //path directly from fd0 or fd1 to fdm1
    //we want timing analysis between clk0 or clk1 and the muxed clock

    //If combinational path consisting of the fanout of two clock domains -> don't care (consider this no timing path exists)
    //If there is a path between FDM0, FDM1 to other ffs, we need create_generated_clock 
    //what it means when clk0 and clk1 interact in the fanout of the mux: these clock domains cross only in the fanout of the mux

    //If there is no timing path between the original clocks and the generated_clocks, no need for create_generated_clock(because we're not doing timing analysis for the generated_clocks), 
    //and use -logically_exclusive for the original clocks because the original clocks don't have timing paths between them

    //However, if a FF driven by a generated_clock or an original clock captures any signal from another clock domain,
    //we need timing analysis between the two clock domains (if one is generated, we use create_generated_clock)
    //to specify that the muxed clocks are physically exclusive (they cannot exist physically at the same time) we use the -physically_exclusive option 
    
    //Combinatorial path involving signals from clk0, clk1, clk_mux
    assign comb1 = fd0_out & fd1_out ^ fdm0_out; 

    //Timing path between clk0 and clk_mux, requires create_generated_clock
    assign comb2 = {fd0_out, 1'b0, fd0_out, 1'b1} + 4'b1010;




endmodule


module mux_2to1(
    input in0,
    input in1,
    input sel,
    output out
);
    assign out = sel ? in0 : in1;
endmodule

//Fixed input mux
module mux_4to1(
    input [1:0] sel,
    output out
);
    always @(*) begin
      case (sel)
        2'b00: out = 1'b0;
        2'b01: out = 1'b0;
        2'b10: out = 1'b1;
        2'b11: out = 1'b1;
        default: out = 1'b0;
      endcase
    end
endmodule

module dff(
    input clk,
    input D,
    output reg Q
);
    always @(posedge clk) begin
        Q <= D;
    end

endmodule
