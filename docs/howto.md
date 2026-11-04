# Karabas Go How-to

How to prepare the newly created devboard to run:

1. Prepare an SD card #1 with cores (*.kg, one file for all the boards) in the root of SD card. The SD card could be FAT16, FAT32 or EXFAT formatted.

2. Upload the RP2040 firmware:

- Press and hold the "RP Boot" button
- Press then release the "RP Reset" button
- Release the "RP Boot" button
- Put the firmware.uf2 into a mounted drive
- Wait a bit until it reboots
- Done, the boot.kg core should starts (the cores need the firmware 26110415 or later: an older one stops with "Boot file not found")

3. Profit

