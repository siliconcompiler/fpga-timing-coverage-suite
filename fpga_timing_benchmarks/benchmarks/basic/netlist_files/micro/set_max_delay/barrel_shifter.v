/*
Circuit Name: barrel_shifter
SDC Name: set_max_delay
Description: 
    -A configurable width barrel shifter circuit.
    -'set_max_delay' will override the default setup requirement.
    -By constraining the 'reg_data_out' with a max delay value, the PnR stage should try to optimize the implementation.
    -The change in slack should be observed as the delay value changes. 
*/

module barrel_shifter #(parameter DATA_WIDTH = 32)(
    input clk,
    input [DATA_WIDTH-1:0] data,
    input shift_left,
    input [$clog2(DATA_WIDTH)-1:0] shift_amt,
    output [DATA_WIDTH-1:0] data_out
);
    reg [DATA_WIDTH-1:0] reg_data_in, reg_data_out;
    wire [DATA_WIDTH-1:0] data_shifted;

    assign data_shifted = shift_left ? data << shift_amt : data >> shift_amt;

    always @(posedge clk) begin
        reg_data_in <= data;
        reg_data_out <= data_shifted;
    end

    assign data_out = reg_data_out;

endmodule