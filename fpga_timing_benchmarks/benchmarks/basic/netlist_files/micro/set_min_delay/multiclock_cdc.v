/*
Circuit Name: multiclock_cdc
SDC Name: set_min_delay
Description: 
    -A 2-stage FF for asynchronous clock domain crossing.
    -Instead of using 'set_clock_groups -asynchronous' or 'set_false_path' to constrain clock domain crossings, 
     one can use 'set_min_delay' to constrain the data crossing two domains so that STA isn't blinded from timing 
     violations that may occur in the design.
    -'set_min_delay' overrides default hold requirements. Because the two clocks may possess uncertainties relative to each other,
     hold violation is a risk when the data paths are too close to each other. Use the 'set_min_delay' constraint to account for the
     potential jitter/uncertainty and ensure hold time is met. 
    -The delay value should be chosen experimentally such that clock uncertainty will not result in hold violations.
     (https://gist.github.com/brabect1/7695ead3d79be47576890bbcd61fe426)
    -Examine the PnR results for different delay values to see how VTR reacts to this constraint.

SDC Example:
    create_clock -period 10.0 [get_ports clk_A]
    create_clock -period 5.0  [get_ports clk_B]     

    set_min_delay 0.5 -from [get_cells data_A_reg] -to [get_cells sync_ff1_reg]
*/

module multiclock_cdc (
    // Domain A (Source)
    input wire clk_A,
    input wire reset_A,
    output reg [3:0] count_A,

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
        count_A <= 4'b0;
    end
    else begin
        count_A <= count_A + 1'b1;
    end
end

// data_A is the MSB of the counter (changes every 8 cycles)
// This is the single-bit signal crossing the clock boundary.
always @(posedge clk_A) begin
    data_A <= count_A[3];
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