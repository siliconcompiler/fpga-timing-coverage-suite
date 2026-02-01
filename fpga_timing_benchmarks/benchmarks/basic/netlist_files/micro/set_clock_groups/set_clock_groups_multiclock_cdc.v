/*
set_clock_groups

example SDC:
create_clock -name clk_A -period 
create_clock -name clk_B -period 

set_clock_groups -group clk_A -group clk_B -asynchronous
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
