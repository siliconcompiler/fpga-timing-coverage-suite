/*
Command: get_ports
Description:
    -Returns a list of all top level ports that match patterns 
    
SDC Example:
    get_ports data*
    get_ports -regexp rst
*/

module get_ports(
    input wire clk,
    input wire rst,
    input wire data1_in,
    input wire data2_in,
    input wire valid_in,
    output reg result_out,
    output wire ready_out
);
    //ready_out is always 1 for this simple module
    assign ready_out = 1'b1;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            result_out <= 1'b0;
        end
        else if (valid_in) begin
            result_out <= data1_in + data2_in;
        end
    end

endmodule