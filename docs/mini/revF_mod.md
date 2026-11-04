### Required HW mod for all revisions before Rev.G:

The latest cores that uses FT812 chip (boot and tsconf) now requires a generated clock by FPGA instead of 8MHz crystal oscillator.
To perform the mod please do the following:

1. Remove the crystal Y3 (8 MHz)
2. Remove capacitors C40, C41 (18 pF)
3. Find a FPGA net MCU_IO4 and connect it to the Y3 pin 1 by a thin wire

<img width="720" height="1280" alt="image" src="https://github.com/user-attachments/assets/6c0353e9-72ee-4333-b9af-bc0b21796d64" />

<img width="859" height="707" alt="image" src="https://github.com/user-attachments/assets/598732b1-598a-4d0c-96e7-f6a9aea87d72" />

