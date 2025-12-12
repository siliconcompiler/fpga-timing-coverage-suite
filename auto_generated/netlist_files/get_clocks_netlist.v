/*
Command: get_clocks
Description:
    -Returns a list of clocks matching patterns
    
SDC Example:
    get_clocks clk1
    get_clocks -quiet clk1098
*/

//Main module
module get_clocks(
    input wire clk1, 
    input wire clk2,
    input wire clk_gen,
    input wire clock,
    output reg dummy_out
);
    initial dummy_out = 1'b1;

    always @(posedge clk1 or posedge clk2 or posedge clk_gen or posedge clock) begin
        dummy_out <= ~dummy_out;
    end

endmodule

