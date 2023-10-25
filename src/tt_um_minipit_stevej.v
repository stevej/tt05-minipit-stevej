`default_nettype none
`timescale 1ns/1ps

module tt_um_minipit_stevej (
    input  wire [7:0] ui_in,    // Dedicated inputs - dedicated to the config bytes
    output wire [7:0] uo_out,   // Dedicated outputs - dedicated to status
    /* verilator lint_off UNUSEDSIGNAL */
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    /* verilator lint_off UNUSEDSIGNAL */
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire reset = ! rst_n;
    wire [7:0] status;

    // registers derived from config byte 0
    reg divider_on;
    reg repeating;
    reg counter_set;
    reg interrupting;
    // registers derived from uio_in;
    wire we;
    assign we = uio_in[0];
    reg [1:0] config_address;

    wire config_address_0;
    assign config_address_0 = uio_in[1];

    wire config_address_1;
    assign config_address_1 = uio_in[2];

    // wherein we need temporary storage
    reg [15:0] temp_counter;

    assign uio_oe = 8'b1111_0000;

    // counter derived from config byte 1 concatenated with config byte 0
    reg [15:0] counter;
    reg [15:0] current_count;

    // If the divider is enabled, 
    reg [8:0] divider_count;

    // uo_out is always a status byte
    assign uo_out = {divider_on, counter_set, 1'b0, 1'b0, interrupting, 1'b0, 1'b0, 1'b0};
    assign uio_out = {1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, 1'b0, interrupting};

    always @(posedge clk) begin
        // if reset, set counter to 0
        if (reset) begin
            counter <= 0;
            current_count <= 0;
            counter_set <= 0;
            divider_on <= 0;
            divider_count <= 0;
        end else begin
            // TODO: set config_address_1, config_address_0, and we
            // set config bits from ui_in;
            if (we) begin
                config_address <= {config_address_1, config_address_0};
                case (config_address)
                    2'b00: begin // write config registers
                        divider_on <= ui_in[7];
                        repeating <= ui_in[6];
                    end
                    2'b01: begin // counter high byte
                        temp_counter <= {ui_in, 8'b0};
                        counter <= counter & temp_counter;
                    end
                    2'b10: begin // counter low byte
                        temp_counter <= {8'b0, ui_in}; 
                        counter <= counter & temp_counter;
                        counter_set <= 1;
                    end
                    2'b11: begin // unused
                    end
                endcase
            end // end config logic

            if (counter_set && divider_on) begin
                divider_count <= divider_count + 1;
                if (divider_count == 10) begin
                    current_count <= current_count + 1;
                end
            end else begin
                `ifdef FORMAL
                    assert(!divider_on);
                `endif
                current_count <= current_count + 1;
            end

            if (counter_set && (current_count == counter)) begin
                // pull interrupt line high for one clock cycle
                interrupting <= 1;
            end else begin
                interrupting <= 0;
            end
        end
    end
endmodule
