/*
Circuit: Asynchronous FIFO
Tests: set_false_path
*/

module async_fifo #(
    parameter DATA_WIDTH = 8,
    parameter ADDR_WIDTH = 4
)(
    input wire wr_clk, wr_rst_n, wr_inc,
    input wire [DATA_WIDTH-1:0] wr_data,
    output wire wr_full, 
    
    input wire rd_clk, rd_rst_n, rd_inc,
    output wire [DATA_WIDTH-1:0] rd_data, 
    output wire rd_empty
);
    wire [ADDR_WIDTH-1:0] wr_addr, rd_addr;
    wire [ADDR_WIDTH:0] wr_ptr, rd_ptr, wr_ptr_sync, rd_ptr_sync;

    two_stage_ff #(.WIDTH(ADDR_WIDTH+1)) rd_to_wr (
        .clk(wr_clk), .rst_n(wr_rst_n), .data_in(rd_ptr), .data_synced(rd_ptr_sync)
    );

    two_stage_ff #(.WIDTH(ADDR_WIDTH+1)) wr_to_rd (
        .clk(rd_clk), .rst_n(rd_rst_n), .data_in(wr_ptr), .data_synced(wr_ptr_sync)
    );

    fifo_mem #(.DATA_WIDTH(DATA_WIDTH), .ADDR_WIDTH(ADDR_WIDTH)) fifomem (
        .wr_clk(wr_clk), .wr_en(wr_inc), .wr_full(wr_full), .wr_data(wr_data), 
        .wr_addr(wr_addr), .rd_addr(rd_addr), .rd_data(rd_data)
    );

    empty_handler #(.ADDR_WIDTH(ADDR_WIDTH)) empty_unit (
        .wr_ptr_sync(wr_ptr_sync), .rd_inc(rd_inc), .rd_clk(rd_clk), .rd_rst_n(rd_rst_n),
        .rd_empty(rd_empty), .rd_addr(rd_addr), .rd_ptr(rd_ptr)
    );

    full_handler #(.ADDR_WIDTH(ADDR_WIDTH)) full_unit (
        .rd_ptr_sync(rd_ptr_sync), .wr_inc(wr_inc), .wr_clk(wr_clk), .wr_rst_n(wr_rst_n),
        .wr_full(wr_full), .wr_addr(wr_addr), .wr_ptr(wr_ptr)
    );

endmodule 

/*
FIFO Memory
*/
module fifo_mem #(
    parameter DATA_WIDTH = 8,
    parameter ADDR_WIDTH = 4
)(
    input wire wr_clk, wr_en, wr_full,
    input wire [DATA_WIDTH-1:0] wr_data,
    input wire [ADDR_WIDTH-1:0] wr_addr, rd_addr,
    output wire [DATA_WIDTH-1:0] rd_data
);
    (* mem2reg *)
    localparam DEPTH = (1 << ADDR_WIDTH);

    reg [DATA_WIDTH-1:0] mem [DEPTH-1:0];
    initial mem[0] <= 255;

    assign rd_data = mem[rd_addr];

    always @(posedge wr_clk) begin
        if (wr_en && !wr_full) mem[wr_addr] <= wr_data;
    end

endmodule 

/*
Two stage synchronizing FF
*/
module two_stage_ff #(
    parameter WIDTH = 4
)(
    input wire clk, rst_n,
    input wire [WIDTH-1:0] data_in,
    output wire [WIDTH-1:0] data_synced
);
    reg [WIDTH-1:0] q1;
    reg [WIDTH-1:0] q2;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q1 <= {WIDTH{1'b0}}; 
            q2 <= {WIDTH{1'b0}};
        end
        else begin
            q1 <= data_in;
            q2 <= q1;
        end
    end

    assign data_synced = q2;

endmodule

/*
read domain 
*/
module empty_handler #(
    parameter ADDR_WIDTH = 4
)(
    input wire [ADDR_WIDTH:0] wr_ptr_sync, 
    input wire rd_inc, rd_clk, rd_rst_n, 

    output reg rd_empty, 
    output wire [ADDR_WIDTH-1:0] rd_addr, 
    output reg [ADDR_WIDTH:0] rd_ptr 
);
    reg [ADDR_WIDTH:0] rd_bin; 
    wire [ADDR_WIDTH:0] rd_bin_next, rd_gray_next; 
    wire empty_val; 

    always @(posedge rd_clk or negedge rd_rst_n) begin
        if (!rd_rst_n) 
            {rd_bin, rd_ptr} <= 0;
        else 
            {rd_bin, rd_ptr} <= {rd_bin_next, rd_gray_next};
    end

    assign rd_addr = rd_bin[ADDR_WIDTH-1:0];
    assign rd_bin_next = rd_bin + (rd_inc & ~rd_empty);
    assign rd_gray_next = (rd_bin_next >> 1) ^ rd_bin_next;
    assign empty_val = (wr_ptr_sync == rd_gray_next); 

    always @(posedge rd_clk or negedge rd_rst_n) begin
        if (!rd_rst_n) 
            rd_empty <= 1'b1;
        else 
            rd_empty <= empty_val;
    end
endmodule

/*
Write domain
*/
module full_handler #(
    parameter ADDR_WIDTH = 4
)( 
    input wire [ADDR_WIDTH:0] rd_ptr_sync,
    input wire wr_inc, wr_clk, wr_rst_n,

    output reg wr_full,
    output wire [ADDR_WIDTH-1:0] wr_addr,
    output reg [ADDR_WIDTH:0] wr_ptr
);
    reg [ADDR_WIDTH:0] wr_bin;
    wire [ADDR_WIDTH:0] wr_bin_next, wr_gray_next;
    wire full_val;
    
    wire [ADDR_WIDTH:0] rd_ptr_inv;
    assign rd_ptr_inv = {~rd_ptr_sync[ADDR_WIDTH:ADDR_WIDTH-1], rd_ptr_sync[ADDR_WIDTH-2:0]};

    always @(posedge wr_clk or negedge wr_rst_n) begin
        if (!wr_rst_n)
            {wr_bin, wr_ptr} <= 0;
        else 
            {wr_bin, wr_ptr} <= {wr_bin_next, wr_gray_next};
    end

    assign wr_addr = wr_bin[ADDR_WIDTH-1:0];
    assign wr_bin_next = wr_bin + (wr_inc & ~wr_full);
    assign wr_gray_next = (wr_bin_next >> 1) ^ wr_bin_next;
    
    assign full_val = (wr_gray_next == rd_ptr_inv);

    always @(posedge wr_clk or negedge wr_rst_n) begin
        if (!wr_rst_n)
            wr_full <= 1'b0;
        else 
            wr_full <= full_val;
    end
endmodule