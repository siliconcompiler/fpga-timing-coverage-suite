module adc_to_dac(
    input clk,
    input [7:0] adc_data,
    output reg [7:0] dac_data
);
     reg [7:0] temp;

     always @(posedge clk) begin
        if(adc_data < 8'b00110000) begin 
            temp <= adc_data * 8'b00000100;
        end
        else begin
            temp <= 8'b0;
        end
        dac_data <= temp; //Use a Low-Pass Filter to filter ambient sound, apply multiplication with a certain factor 
     end

endmodule