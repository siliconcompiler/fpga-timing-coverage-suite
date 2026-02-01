set_max_delay에 CDC (handshake) 추가
set_mind_delay는 뭐가 좋을지 고민. A circuit that requires hold time. A circuit that has a long combinational path so it requires a long propagation path. 
set_min_delay tells the tool to ensure the data doesn't arrive to early
Maybe a dummy pipeline of a simple ALU can do the job (the EX stage of a processor)


set_max_delay: barrel shifter, CDC, 
set_min_delay: very fast pipeline, CDC

few elements between two sequential elements: if clock latency is high, data from the previous cycle may arrive too fast (maybe in the same clock cycle) It would be nice to actually run the fully implemented circuit

/*

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