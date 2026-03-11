/*
Circuit Name: adc_to_dac
SDC Name: set_clock_latency
Description: 
    -A circuit that performs simple data processing to an input data.
    -Apply the 'set_clock_latency -source' constraint along with 'set_input_delay' 
     and 'set_output_delay'. PnR should reflect this additional latency information or 
     there should be changes in slack.  
*/

module adc_to_dac(
    input clk,
    input [7:0] adc_data,
    output reg [7:0] dac_data
);
    reg [7:0] temp;

    // Simple data processing
    always @(posedge clk) begin
        if(adc_data < 8'b00110000) begin 
            temp <= adc_data * 8'b00000100;
        end
        else begin
            temp <= 8'b0;
        end
        dac_data <= temp;
    end
endmodule