import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles


@cocotb.test()
async def test_no_config(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

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
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    dut.uio_in.value = 0xC0  # set we high and config_address_0 to 1
    # counter high byte for 1 cycle
    dut.ui_in.value = 0x01
    await ClockCycles(dut.clk, 1)

    dut.uio_in.value = 0xA0  # set we high and config_address_1 to 1
    dut.ui_in.value = 0x00
    await ClockCycles(dut.clk, 10)

    dut._log.info("checking that interrupt is high")
    assert dut.uo_out.value == 0b01000000
