![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/wokwi_test/badge.svg)

# Small Programmable Interrupt Timer

TinyTapeout is an educational project that aims to make it easier and cheaper than ever to get your digital designs manufactured on a real chip! This is my submission for TinyTapeout 5 in early November 2023.

A programmable interrupt timer allows you to specify when a digital line is pulled high after a given number of clock ticks, the timer can either repeat or be one-shot.

TODO: how to configure the first register
TODO: how to configure the second register, the high byte of the counter
TODO: how to configure the third register, the low byte of the counter.

## Starting the timer.
Configuring the third register is what starts the timer as the other two registers are optional. The default settings if the first register isn't set are to be a one-shot timer with no clock divider.

## RTL errata



# Want to see your own digital design taped out to an ASIC?
Go to https://tinytapeout.com for instructions!