# Karabas Go, Mini, Mini G: how-to

How to prepare a newly built board to run.

## 1. SD card #1

Copy the cores (`cores/*.kg`, one file per core for all the boards) to the root of SD card #1:
FAT16, FAT32 or exFAT. `boot.kg` is the core browser started at power on. Optional: USB
gamepad drivers (a `drivers` directory with `.ini` files) and `karabas.ini` (settings), see
[karabas-go-firmware](https://github.com/andykarpov/karabas-go-firmware).

## 2. The RP2040 firmware

The firmware of the board from `firmware/` (26110415 or later reads the `.kg` cores; an older
one stops with "Boot file not found"):

| Board | Firmware |
| --- | --- |
| Karabas Go | `karabas_go.uf2` |
| Karabas Mini, rev.C .. rev.F3 | `karabas_mini.uf2` |
| Karabas Mini G, rev.G / G2 | `karabas_minig.uf2` |

- Press and hold the "RP Boot" button
- Press then release the "RP Reset" button
- Release the "RP Boot" button
- Copy the `.uf2` of the board to the mounted `RPI-RP2` drive
- Wait a bit until it reboots: the core browser (`boot.kg`) starts

A board that already runs a firmware can also be put into BOOTSEL without the button: the
`bootsel` button action of a core, or `AT+KARABAS=boot` on its USB serial port.

Read the manual of each core about what goes onto SD card #2.

## 3. Mini G: the ESP32-S3 of the shield

`firmware/esp32-s3/` (`firmware/esp32-s3-old-zifi/`: the older ZiFi build):

- Close jumper JP11
- Power the main board with USB-C
- Connect a secondary USB-C cable to the upper board
- Run `flash.bat` (Windows) or `flash.sh` (Linux, macOS; needs `esptool`: `pip install esptool`).
  They find the ESP32-S3 by its USB id (Espressif, VID 303A); if it is not found, or there are
  several, give the port: `flash.bat COM5`, `./flash.sh /dev/ttyACM1`
- After a successful flash, remove the JP11 jumper, disconnect both USB-C cables

The firmware in `firmware/esp32-s3/` (2026-11-25) is ZiFi32 of tslabs/zx-evo `master` plus the fixes
of [andykarpov/zx-evo `karabas/esp32-release`](https://github.com/andykarpov/zx-evo/tree/karabas/esp32-release):
upstream PRs [tslabs/zx-evo#94](https://github.com/tslabs/zx-evo/pull/94) and
[#96](https://github.com/tslabs/zx-evo/pull/96). They fix:

- hangs: RESET / REBOOT of the host now reach the ESP while a command hangs, the stream reader
  could deadlock, Gopher waited for ever on a silent host;
- leaks;
- stalled downloads;
- Wi-Fi connects that never got an IP;
- XM modules which hung or crashed the player (song length 256, loops of length 0, loops past the
  sample, more than 12 envelope points, 16-bit samples of odd length).

Before flashing it over an older build:

- The partition table changed: `fat` 7 MB, `tsf` 5 MB and `oplrom` 2 MB, where the older one had
  `spiffs` and an 8 MB `fat`. What the older `fat` / `spiffs` held is lost. Save the whole flash first
  if needed: `esptool --chip esp32s3 -p <port> read-flash 0 0x1000000 backup.bin`.
- The player commands of the ESP changed (XM / MOD / S3M). Take the matching files from `software/`:
  - `FTVIEW.WMF`: the Wild Commander plugin that plays XM; goes into the `WC` folder.
  - `gopher_esp32.spg`: the Gopher browser, a binary patch of its 2026-04-27 build (the author has
    not published the sources). Patched: the new player codes, the file size taken by GOPHER_GET, a
    longer wait after a DMA read.

## Mini rev.C, D, F: the FT812 clock mod

The cores that use the FT812 (boot, tsconf) need the hardware mod of
[docs/mini/revF_mod.md](mini/revF_mod.md) on the Mini boards before rev.G.

## Mini G rev.G2: the SDRAM ~CS mod

On rev.G2 the SDRAM ~CS has to be tied to GND by hand, otherwise no core that uses the SDRAM works:
[docs/mini/revG2_mod.md](mini/revG2_mod.md).
