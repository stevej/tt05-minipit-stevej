![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/wokwi_test/badge.svg)

# Small Programmable Interrupt Timer

TinyTapeout is an educational project that aims to make it easier and cheaper than ever to get your digital designs manufactured on a real chip! This is my submission for TinyTapeout 5 in early November 2023.

This design is a programmable interrupt timer allows you to specify when a digital line is pulled high after a given number of clock ticks, the timer can either repeat or be one-shot.

This started as a reimplementation of the Intel 8253 programmable interrupt timer and I eventually stripped it down to the bare minimal configuration and wires required to be functional within the wire and gate constraints of a TinyTapeout project.

## Quickstart

The following is pseudocode for configuring an interrupt pin to go high for one cycle after 10 cycles (plus 2 for setup).

```
uio_in = 0xA0
ui_in = 0xA
```

This will set the interrupt timer to be one-shot and set a 8-bit counter of 0xA (integer 10). Wait 12 cycles and then the last pin in `uio_out` will be high.

## More details

There are three configuration registers, written to the data held in `ui_in` and selected with the high 3 bits from `uio_in`:

`uio_in[7]` sets write enable (`WE`), which says the timer is being configured when pulled high.

The concatenation of `{uio_in[5], uio_in[6]}` selects which register is being written.

### Register Selection Values

As previously stated, `{uio_in[5], uio_in[6]}` are the two bits used to select how to configure the timer. The meanings of the four registers are given below:

* `00` sets the options: divider on and repeating
* `01` sets the high bit
* `10` sets the low bit
* `11` is unused

### Timer options

When you select the `00` register, there are only two options available:

#### Clock divider

`divider_on <= ui_in[7];`

This bit selects whether a 10x clock divider is used.

#### Repeating

`repeating <= ui_in[6];`

This bit selects if you want the interrupt to repeat. The default value is for the interrupt to be one-shot.

## Timer registers

The registers selected with `01` and `10` each specify which 8-bits of the 16-bit register to set.

The bits of `01` followed by the bits of `10` determine the full 16-bits of the timer value. `01` does not need to be set if you don't need more than 8-bits but `10` must be set, if only to zero, for the timer to start.
 
## Starting the timer.
Configuring the third register (`10`) is what starts the timer as the other two registers are optional. The default settings if the first register isn't set are to be a one-shot timer with no clock divider.

## Lessons Learned

Programmed IO setup is annoying and I spent a lot of time on it. I think I would prefer to use an SPI ROM or RAM and utilize more of a memory-mapped approach in the future.

I don't have a lot of tools in my toolbox for squeezing cycles out of a design that leans on registers which leads me to the RTL errata section.

## RTL errata

No matter how long the timer is set for, there are a few extra cycles due to setup or latching.

# Want to see your own digital design taped out to an ASIC?
Go to https://tinytapeout.com for instructions!