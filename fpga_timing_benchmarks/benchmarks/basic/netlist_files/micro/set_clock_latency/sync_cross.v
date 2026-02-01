/*
Two synchronous, but out-of-phase clocks driving two registers.
The combinational path between the registers are subject to STA
*/
module sync_cross(
    input clk0,
    input clk1,
    input [63:0] a, 
    input [63:0] b,
    output [63:0] sum
);
    reg [63:0] reg_a, reg_b;
    reg [63:0] sum; 
    wire [63:0] fa_out;

    //clk0 clocks the input registers
    always @(posedge clk0) begin
        reg_a <= a;
        reg_b <= b;  
    end
    
    //Combinational, carry logic left out for simplicity
    assign fa_out = reg_a + reg_b;

    //clk1 clocks the sum register
    always @(posedge clk1) begin
        sum <= fa_out;
    end
endmodule

/*
SDC example
create_clock -period 10.0 [get_ports clk0]
create_clock -period 10.0 [get_ports clk1]

set_clock_latency -source 1.0 [get_ports clk0]
set_clock_latency -source 0.5 [get_ports clk1]

set_input_delay -clock clk0 0 {[get_ports a] [get_ports b]}
set_output_delay -clock clk1 0 [get_ports sum]
Two synchronous clocks that have different source latencies. STA should reflect the change in slack
*/