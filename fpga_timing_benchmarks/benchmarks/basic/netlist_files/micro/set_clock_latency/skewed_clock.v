/*
Circuit Name: skewed_clock
SDC Name: set_clock_latency
Description: 
    -Two synchronous, but out-of-phase clocks are driving different 64-bit registers. 
    -Use 'set_clock_latency' to specify different latencies for each clock pin.
    -The combinational path between the registers is subject to STA. The change in slack should be reported.

SDC example:
    create_clock -period 10.0 [get_ports clk]

    set_clock_latency 1.0 [get_pins reg_a/clk]
    set_clock_latency 1.0 [get_pins reg_b/clk]
    set_clock_latency 2.0 [get_pins reg_sum/clk]

    set_input_delay -clock clk 0 [get_ports {a[*] b[*]}]
    set_output_delay -clock clk 0 [get_ports {sum[*]}]
*/
// Top module
module skewed_clock(
    input clk,
    input [63:0] a, 
    input [63:0] b,
    output [63:0] sum
);
    wire [63:0] wire_a, wire_b;
    wire [63:0] fa_out;

    // Registers for input a and b
    dff_64 reg_a(
        .clk(clk),
        .D(a),
        .Q(wire_a)
    );

    dff_64 reg_b(
        .clk(clk),
        .D(b),
        .Q(wire_b)
    );

    // Combinational, carry logic left out for simplicity
    assign fa_out = wire_a + wire_b;

    // Register for the sum
    dff_64 reg_sum(
        .clk(clk),
        .D(fa_out),
        .Q(sum)
    );

endmodule

// 64-bit DFF
module dff_64(
    input clk,
    input [63:0] D,
    output reg [63:0] Q
);
    always @(posedge clk) begin
        Q <= D;
    end
endmodule