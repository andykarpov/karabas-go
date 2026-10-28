# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

The release repo of the Karabas Go board (Xilinx Spartan-6 XC6SLX25, RP2040 MCU, FT812, VGA, floppy port): what goes onto the SD card and the board, plus the hardware documents. There is no source code and nothing to build here. The cores are built in their own repos (`karabas-go-core-*`, listed in `README.md`), the MCU firmware in `karabas-go-firmware`, the PCB sources in `karabas-go-pcb`. The hardware design and docs are CC BY-NC-SA 4.0 (`LICENSE`); cores and firmware have their own licenses.

## Layout

- `cores/`: the core files `*.kg1` (the Go format, `HW_ID` 1), one per core (`boot.kg1` is the boot menu). They go into the root of SD card 1 (FAT16, FAT32 or exFAT, `docs/howto.md`).
- `firmware/firmware.uf2`: the RP2040 firmware, copied to the `RPI-RP2` drive in BOOTSEL.
- `software/`: extra files for the cores (`TBBLUE.FW`, the ZX Next firmware).
- `docs/`: `howto.md` (first start), the schematics (`karabas-go-rev*.pdf`) and interactive BOMs (`*-ibom.html`) of each PCB revision and of the Dream add-on, the renders used by `README.md`.
- `pcb/`: the gerbers (`*-gerbers.zip`) of each revision, the add-on and the extender. `PCB_CHANGELOG.md`: the revisions (latest Rev.B4, Rev.C dev in progress).
- `case/`: 3D enclosure models (STL and others) by several authors.

## Release

- `firmware/firmware.uf2` is committed by the CI release job of `karabas-go-firmware` (`.github/workflows/build.yml`, the `SIBLING_REPOS_TOKEN` secret, commits "Firmware build <version>: ..." by github-actions[bot]). Never commit the firmware by hand. The job also removes `cores/karabas.ini`, `firmware/karabas.ini` and `firmware/drivers` if they appear: the firmware has the defaults.
- Core files are copied in by hand after a core release: the `.kg1` built and committed by the core repo replaces the one in `cores/`. Commit messages follow "<Core> build <date stamp>: <what changed>" (e.g. "Spec256 build 26102321: ..."). The `.kg2` / `.kg3` of the same release go to the sibling repo `karabas-mini` (`cores/`).
- The CI job pushes with `git pull --rebase`: pull before committing a core, the firmware may have moved on.
- Commit only the files of the release. Do not commit untracked user files (local `karabas.ini`, drivers, test images).
- Do not touch `case/`, `pcb/` and the PCB documents unless asked: they come from the hardware work, not from the cores or the firmware.

## Memory

The Claude Code memory of this repo is shared with all karabas-go repos: `~/.claude/projects/<this project>/memory` is a symlink to `../karabas-go-notes` (private repo `andykarpov/karabas-go-notes`, `link.sh` there makes the links). Its `MEMORY.md` is split by repo; commit and push it after every memory change.
