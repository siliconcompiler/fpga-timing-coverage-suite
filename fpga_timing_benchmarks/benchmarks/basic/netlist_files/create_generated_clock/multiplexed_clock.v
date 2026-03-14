/*
Circuit Name: multiplexed_clock
SDC Name: create_generated_clock
Description: 
    -Two independent clocks clk0 and clk1 is selected using a MUX. Three clocks drive different registers and there are timing paths between them. 
    -The timing path between clk0 and clk_mux should be analyzed and requires 'create_generated_clock' to indicate that clk_mux is a generated clock. 
    -The combinational path combining domains clk0, clk1 and clk_mux isn't clocked. And doesn't require timing analysis.
    -Because the two clocks defined at the fanout of the MUX cannot coexist, prevent unnecessary analysis with 'set_clock_groups -physically_exclusive'.
    -Because clk0 and clk1 don't have timing paths between them, use 'set_clock_groups -logically_exclusive'.

SDC Example:
    create_clock -period 10.0 [get_ports clk0]
    create_clock -period 12.0 [get_ports clk1]

    create_generated_clock -name clk0mux -divide_by 1 -source [get_pins clock_mux/in0] [get_pins clock_mux/out]
    create_generated_clock -name clk1mux -divide_by 1 -add -master_clock [get_clocks clk1] -source [get_pins clock_mux/in1] [get_pins clock_mux/out]

    set_clock_groups -logically_exclusive -group [get_clocks clk0] -group [get_clocks clk1]
    set_clock_groups -physically_exclusive -group [get_clocks clk0mux] -group [get_clocks clk1mux]

    // Clock delay due to mux
    set_clock_latency 0.5 [get_clocks {clk0mux clk1mux}]
*/

// Top module
module multiplexed_clk(
    input clk0,
    input clk1,
    input sel,
    input a,
    input b,
    output comb1, 
    output fdm1_out
);
    wire clk_mux;
    wire fd0_out, fd1_out, fdm0_out;
    wire [3:0] comb2;

    // clk0 domain
    dff FD0(
        .clk(clk0),
        .D(a),
        .Q(fd0_out)
    );
    // clk1 domain
    dff FD1(
        .clk(clk1),
        .D(a),
        .Q(fd1_out)
    );

    // Muxed domain
    dff FDM0(
        .clk(clk_mux),
        .D(a),
        .Q(fdm0_out)
    );
    dff FDM1(
        .clk(clk_mux),
        .D(comb2[3]),
        .Q(fdm1_out)
    );
    
    // Clock mux
    mux_2to1 clock_mux(
        .in0(clk0),
        .in1(clk1),
        .sel(sel),
        .out(clk_mux)
    );
    
    // Combinational path involving signals from domains clk0, clk1, clk_mux
    // This path is logically unconstrained
    assign comb1 = fd0_out & fd1_out ^ fdm0_out; 

    // Timing path between clk0 and clk_mux, requires create_generated_clock to calculate setup/hold requirements
    assign comb2 = {fd0_out, 1'b0, fd0_out, 1'b1} + 4'b1010;

endmodule

// 2to1 MUX
module mux_2to1(
    input in0,
    input in1,
    input sel,
    output out
);
    assign out = sel ? in1 : in0;
endmodule

// DFF
module dff(
    input clk,
    input D,
    output reg Q
);
    always @(posedge clk) begin
        Q <= D;
    end

endmodule
