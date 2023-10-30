import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles


@cocotb.test()
async def test_no_config(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.uio_out.value = 0x0
    dut.uio_in.value = 0x0
    dut.uo_out.value = 0x0

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 0x00
    dut.ui_in.value = 0x80  # set we high

    await ClockCycles(dut.clk, 10)
    dut._log.info("checking that interrupt is not high")
    assert dut.uo_out.value == 0x00


@cocotb.test()
async def test_one_shot(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)

    dut.rst_n.value = 1
    dut.uio_in.value = 0xC0  # set we high and config_address to 0b01
    dut.ui_in.value = 0x00  # should not set temp_counter
    await ClockCycles(dut.clk, 2)

    dut.uio_in.value = 0xA0  # set we high and config_address to 0b10
    dut.ui_in.value = 0x0A
    await ClockCycles(dut.clk, 10)
    dut.uio_in.value = 0x0  # unset we so we no longer configure registers.
    await ClockCycles(dut.clk, 10)

    dut._log.info("checking that interrupt is high")
    assert dut.uo_out.value == 0b01000000


@cocotb.test()
async def repeating_no_divider(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)

    dut.rst_n.value = 1
    # set WE high, config_address to 0b00
    dut.uio_in.value = 0b1000_0000
    # divider off, repeat on.
    dut.ui_in.value = 0b0100_0000
    # TODO: set repeating on in the payload
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 0x01
    dut.ui_in.value = 0x00
    # set WE high and config_address to 0b01
    dut.uio_in.value = 0xC0
    dut.ui_in.value = 0x00  # should not set temp_counter
    await ClockCycles(dut.clk, 2)

    dut.uio_in.value = 0xA0  # set we high and config_address to 0b10
    dut.ui_in.value = 0x0A
    await ClockCycles(dut.clk, 13)
    dut._log.info("checking that interrupt is high")
    assert dut.uo_out.value == 0b01001000
    assert dut.uio_out.value == 0b0000_0001

    dut.uio_in.value = 0x0  # unset we so we no longer configure registers.
    await ClockCycles(dut.clk, 11)
    dut._log.info("checking that interrupt is high")
    assert dut.uo_out.value == 0b01001000
    assert dut.uio_out.value == 0b0000_0001


@cocotb.test()
async def oneshot_divided(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # reset
    dut._log.info("reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)

    dut.rst_n.value = 1

    dut.uio_in.value = 0x80  # set we high and config_address to 0b00
    dut.ui_in.value = 0x80  # set divider to on, repeating off
    await ClockCycles(dut.clk, 2)

    dut.uio_in.value = 0xC0  # set we high and config_address to 0b01
    dut.ui_in.value = 0x00  # should not set temp_counter
    await ClockCycles(dut.clk, 2)

    dut.uio_in.value = 0xA0  # set we high and config_address to 0b10
    dut.ui_in.value = 0x01  # wait one cycle, with a divider will be 10 cycles
    await ClockCycles(dut.clk, 14)
    dut.uio_in.value = 0x0  # unset we so we no longer configure registers.

    dut._log.info("checking that interrupt is high")
    assert dut.uo_out.value == 0b1100_1000
