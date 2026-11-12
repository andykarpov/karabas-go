# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

The release repo of the Karabas Go family: Karabas Go, Karabas Mini and Mini G (Xilinx Spartan-6 XC6SLX25, RP2040 MCU, FT812; Go: VGA, floppy port; Mini / Mini G: HDMI/DVI, ESP8266, an ESP32-S3 on the Mini G shield). What goes onto the SD card and the boards, plus the hardware documents of all the boards. There is no source code and nothing to build here. The cores are built in their own repos (`karabas-go-core-*`, listed in `README.md`), the MCU firmware in `karabas-go-firmware`, the PCB sources in `karabas-go-pcb` / `karabas-mini-pcb`. The hardware design and docs are CC BY-NC-SA 4.0 (`LICENSE`); cores and firmware have their own licenses. The former `karabas-mini` repo is archived (its README points here); its files were copied in without their history (2026-11-04).

## Layout

- `cores/`: the core files `*.kg`, one per core with the bitstreams of all the boards (format kgo2, karabas-go-tools `docs/kgo2.md`; `boot.kg` is the boot menu). They need the firmware 26110415 or later, an older firmware does not see them and stops with "Boot file not found". They go into the root of SD card 1 (FAT16, FAT32 or exFAT, `docs/howto.md`).
- `firmware/karabas_go.uf2`, `karabas_mini.uf2` (Mini rev.C .. F3), `karabas_minig.uf2` (Mini G rev.G / G2): the RP2040 firmware, copied to the `RPI-RP2` drive in BOOTSEL. `firmware/esp32-s3/`: the ESP32-S3 firmware of the Mini G shield (`flash.sh` / `flash.bat`, JP11 closed while flashing); `esp32-s3-old-zifi/` the older ZiFi build.
- `software/`: extra files for the cores (`TBBLUE.FW` of ZX Next, `.WMF` plugins, `gopher_esp32.spg`).
- `docs/howto.md` (first start, all boards); `docs/go/`, `docs/mini/`: schematics (`*-rev*.pdf`), interactive BOMs (`*-ibom.html`), the renders of `README.md`; `docs/mini/revF_mod.md`: the FT812 clock mod of Mini rev.C, D, F; `docs/mini/revG2_mod.md` (+ photo): the SDRAM ~CS mod of rev.G2.
- `pcb/go/`, `pcb/mini/`: gerbers (`*-gerbers.zip`) of each revision, add-on, extender and shield, each with its `PCB_CHANGELOG.md` (Go: Rev.B4, Rev.C dev; Mini: Rev.G stable, then G2).
- `case/go/`, `case/mini/`: 3D enclosure models by several authors.

## Release

- `firmware/karabas_*.uf2` are committed by the CI release job of `karabas-go-firmware` (`.github/workflows/build.yml`, the `SIBLING_REPOS_TOKEN` secret, commits "Firmware build <version>: ..." by github-actions[bot]). Never commit them by hand. The job also removes `cores/karabas.ini`, `firmware/karabas.ini` and `firmware/drivers` if they appear: the firmware has the defaults. The ESP32-S3 files are not touched by the job.
- Core files come in by CI: `.github/workflows/sync-cores.yml` (every hour at :23, and by hand: Actions > Sync cores > Run workflow, optionally one file) runs `.github/scripts/sync_cores.py`, which downloads the `.kg` of each core of `cores.json` (repo, branch, path; the core repos are public, no secret) and, when it differs from `cores/` and is a valid kgo2 file with the same core id, commits it as "<Core name> build <build>: <subject of the core commit> (<repo>@<sha>)" (one commit per core). A core release is thus: commit the new `.kg` in the core repo, merge; it shows up here within the hour. A new core = a line in `cores.json` and in the Sources of both `README.md` and `README.ru.md` (Russian, keep them in step). `pong.kg` (Go only) has no core repo and is not synced: it was converted from the old `pong.kg1` (karabas-go-tools `kg1_to_json.py`). Copying a core by hand still works (the next sync sees it equal).
- Both CI jobs (firmware, sync cores) push with `git pull --rebase`: pull before committing anything by hand.
- Commit only the files of the release. Do not commit untracked user files (local `karabas.ini`, drivers, test images).
- Do not touch `case/`, `pcb/` and the PCB documents unless asked: they come from the hardware work, not from the cores or the firmware.

## Memory

The Claude Code memory of this repo is shared with all karabas-go repos: `~/.claude/projects/<this project>/memory` is a symlink to `../karabas-go-notes` (private repo `andykarpov/karabas-go-notes`, `link.sh` there makes the links). Its `MEMORY.md` is split by repo; commit and push it after every memory change.
