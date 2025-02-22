# Karabas-Go

A Spartan-6 based devboard to emulate different retro-computers.

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

The hardware design and documentation are licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](http://creativecommons.org/licenses/by-nc-sa/4.0/).

FPGA cores, the firmware and other software parts are licensed by their own licenses.

### What's on the board:

- A 25k LE's Spartan-6 FPGA
- RP2040 MCU
- 4x USB Ports
- 2x 2MB 10ns SRAM chips
- 32MB SDRAM chip
- VGA 8:8:8 output
- On-board FT812 video processor
- 16-bit audio DAC
- SAM2695 midi synth
- 2x Sega/Atari compatible DB9 joystick ports
- CF card
- 2x microSD cards
- Tape In/Out interface
- FDD port
- Buzzer
- DS3221 RTC
- 1kB EEPROM
- ESP8266 Wi-Fi module

### PCB 

The latest PCB revision number is Rev.B4.
PCB Changelog: https://github.com/andykarpov/karabas-go/blob/master/PCB_CHANGELOG.md

Warning: Rev.B4 could be a bit incompatible with the 3D enclosure models due to microSD cards shifted a bit forward.

### FPGA Core Sources

- Boot Menu Core: https://github.com/andykarpov/karabas-go-core-menu
- Test Core: https://github.com/andykarpov/karabas-go-core-test
- TS-Conf Core: https://github.com/andykarpov/karabas-go-core-tsconf
- ZX Spectrum Next Core: https://github.com/andykarpov/karabas-go-core-next
- Karabas Pro Core: https://github.com/andykarpov/karabas-go-core-profi
- PCXT Core: https://github.com/andykarpov/karabas-go-core-pcxt
- NES Core: https://github.com/andykarpov/karabas-go-core-nes
- Radio RK86 Core: https://github.com/andykarpov/karabas-go-core-rk86
- Alf Core: https://github.com/andykarpov/karabas-go-core-alf

### The Firmware Sources

- https://github.com/andykarpov/karabas-go-firmware

### Dev Tools

- https://github.com/andykarpov/karabas-go-tools

### Pre-production renders:

![image](https://github.com/andykarpov/karabas-go/blob/master/docs/karabas-go-top.png?raw=true)

![image](https://github.com/andykarpov/karabas-go/blob/master/docs/karabas-go-bot.png?raw=true)
