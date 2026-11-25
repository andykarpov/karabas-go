#!/bin/bash
# Writes this ZiFi32 build into the ESP32-S3 of the Mini G shield (docs/howto.md, section 3).
# The port: ./flash.sh /dev/ttyACM1 (or PORT=...); without it the ESP32-S3 is found by its
# USB id, /dev/serial/by-id/usb-Espressif_* (the USB-Serial/JTAG of the chip, VID 303A).
set -e
cd "$(dirname "$0")"
PORT=${1:-$PORT}
if [ -z "$PORT" ]; then
  ports=(/dev/serial/by-id/usb-Espressif_*)
  if [ ! -e "${ports[0]}" ]; then
    echo "No ESP32-S3 on USB (/dev/serial/by-id/usb-Espressif_*)."
    echo "Connect it (docs/howto.md), or give its port: $0 /dev/ttyUSB0"
    ls /dev/serial/by-id/ 2>/dev/null | sed 's/^/  seen: /'
    exit 1
  fi
  if [ ${#ports[@]} -gt 1 ]; then
    echo "More than one ESP32 on USB, give the port:"
    printf '  %s\n' "${ports[@]}"
    exit 1
  fi
  PORT=$(readlink -f "${ports[0]}")
fi
ESPTOOL=$(command -v esptool || command -v esptool.py) || { echo "esptool not found: pip install esptool"; exit 1; }
echo "ESP32-S3 on $PORT"
"$ESPTOOL" --chip esp32s3 --port "$PORT" -b 460800 --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size detect --flash_freq 80m \
  0x0 bootloader.bin 0x8000 partition-table.bin 0x10000 esp-spi.bin
