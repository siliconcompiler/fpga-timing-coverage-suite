/*
Command: set_disable_timing
Description:
    -Disables timing through paths specified by the command
    
SDC Example:
    set_disable_timing -from [get_ports d_in_1] -to [get_ports d_out_1] u1
    set_disable_timing u1
*/

//Main module
module set_disable_timing(
    input wire clk,
    input wire d_in_1,
    input wire d_in_2,
    output wire d_out_1, 
    output reg d_out_2
);
    comb u1(.a(d_in_1), .b(d_in_2), .y(d_out_1));

    always @(posedge clk) begin
        d_out_2 <= d_in_1;
    end

endmodule

module comb (
    input wire a,
    input wire b,
    output wire y
);
    assign y = a & b;
endmodule