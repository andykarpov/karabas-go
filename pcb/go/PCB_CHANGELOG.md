## Rev.C dev

- A development edition with ESP32 on board
- Cleanup, removed unused stuff
- Added ESP32-S3 module with connection to the FT QSPI and FPGA as I2S slave
-- ESP32 I2S bus connected to the unused conf flash pins CONF_IO0, CONF_IO2, CONF_IO3
-- ESP32_SPI_CS pin will use a ESP_BOOT or UART_CTS (this is an open question yet, a set of jumpers is exists to decide later)

Please do not use this version yet. The development is in progress...

## Rev.B4

- Moved CF card deeper
- Textual fixes on the bottom silkscreen
- Added THT RGB LEDs in parallel to the smd ones
- Replaced FPC connector for external SD cards to a pin headers 1.27mm pitch

## Rev.B3

- Cleanup
- Changed USB-A footprints
- Moved USB-A connectors 1mm deeper
- Moved USB-C and audio TRS connectors a bit out of the board

## Rev.B2

- Added FPC connectors for external SD cards
- Added FPC connector for slim FDD
- Added FT_PD ext reset, routed to MCU
- Added midi chip
- Added Op Amp to the sound output

## Rev.B1

- Added universal footprint for the ADV7125
- Fixed FE1.1s footprint
- Updated buzzer footprint
- Added alternate footprint for the DS3231M IC
- Added bus between MCU and FPGA
- Increased power rails width
- Swapped test points to a bottom side
- Replaced FPGA 0402 caps with 0603 caps

## Rev.B

- Bugfix revision
- Changed incorrect FT buffers direction
- Added missing power line to the RP2040
- Fixed some values

## Rev.A

- Initial Revision
