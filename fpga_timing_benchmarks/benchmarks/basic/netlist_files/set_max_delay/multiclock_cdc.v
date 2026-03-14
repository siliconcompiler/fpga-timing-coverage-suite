/*
Circuit Name: multiclock_cdc
SDC Name: set_max_delay
Description: 
    -A 2-stage FF for asynchronous clock domain crossing.
    -Instead of using 'set_clock_groups -asynchronous' or 'set_false_path' to constrain clock domain crossings, 
     one can use 'set_max_delay' to constrain the data crossing two domains so that STA isn't blinded from timing 
     violations that may occur in the design.
    -The delay value should be chosen so that the path will meet timing without relaxing it too much. The delay 
     value is to be chosen experimentally for each technology. A good rule of thumb is to use the clock period for 
     the max delay value, or choosing the minimum of the source and destination clock. 
     (https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Constraints-on-Individual-CDC-Paths)
    -Examine the PnR results for different delay values to see how VTR reacts to this constraint. 

SDC Example:
    create_clock -period 10.0 [get_ports clk_A]
    create_clock -period 5.0  [get_ports clk_B]     

    set_max_delay 5.0 -from [get_cells data_A_reg] -to [get_cells sync_ff1_reg]
*/

module multiclock_cdc #(parameter WIDTH = 4)(
    // Domain A (Source)
    input wire clk_A,
    input wire reset_A,
    output reg [WIDTH-1:0] count_A,

    // Domain B (Destination)
    input wire clk_B,
    input wire reset_B,
    output reg sync_data_B
);

// --- 1. Domain A Logic (Source) ---

// An internal signal in Domain A that we want to transfer
reg data_A; 

always @(posedge clk_A or posedge reset_A) begin
    if (reset_A) begin
        count_A <= 0;
    end
    else begin
        count_A <= count_A + 1'b1;
    end
end

// data_A is the MSB of the counter (changes every 8 cycles)
// This is the single-bit signal crossing the clock boundary.
always @(posedge clk_A) begin
    data_A <= count_A[WIDTH-1];
end

// --- 2. Two-Flip-Flop (2-FF) Synchronizer ---

// These are the two synchronizing registers, clocked by the DESTINATION clock (clk_B)
reg sync_ff1;
reg sync_ff2;

// The first FF captures the ASYNCHRONOUS input (data_A) on the destination clock
always @(posedge clk_B or posedge reset_B) begin
    if (reset_B) begin
        sync_ff1 <= 1'b0;
        sync_ff2 <= 1'b0;
    end
    else begin
        // The first FF samples the incoming data from Domain A
        sync_ff1 <= data_A; 
        
        // The second FF samples the output of the first FF
        sync_ff2 <= sync_ff1;
    end
end

// The synchronized signal for use in Domain B
always @(posedge clk_B) begin
    sync_data_B <= sync_ff2;
end

endmodule
