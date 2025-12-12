/*
Command: get_pins
Description:
    -Returns a list of all instance pins matching patterns
    
SDC Example:
    get_pins -regexp u1/D
    get_pins u1/D
*/

//Main module
module get_pins(
    input wire clk, 
    input wire data_in,
    output reg [1:0] data_out
);
    wire u1_out, u2_out;

    //Datapath
    DFF u1(.clk(clk), .D(data_in), .Q(u1_out));
    DFF u2(.clk(clk), .D(~data_in), .Q(u2_out));

    assign data_out = {u1_out, u2_out};

endmodule

module DFF(
    input wire clk,
    input wire D,
    output reg Q
);
    always @(posedge clk) begin
        Q <= D;
    end
endmodule