/*
set_max_delay: overrides default setup requirement

sample SDC
set_max_delay -from -to
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

    if (shift_left) begin
        assign data_shifted = data << shift_amt;
    end
    else begin
        assign data_shifted = data >> shift_amt;
    end

    always @(posedge clk) begin
        reg_data_in <= data;
        reg_data_out <= data_shifted;
    end

    assign data_out = reg_data_out;

endmodule