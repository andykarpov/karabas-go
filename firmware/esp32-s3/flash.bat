@echo off
rem Writes this ZiFi32 build into the ESP32-S3 of the Mini G shield (docs\howto.md, section 3).
rem The port: flash.bat COM5; without it the ESP32-S3 is found by its USB id
rem (the USB-Serial/JTAG of the chip, VID 303A).
cd /d "%~dp0"
set PORT=%1
if "%PORT%"=="" for /f "usebackq delims=" %%p in (`powershell -NoProfile -Command "Get-CimInstance Win32_PnPEntity | Where-Object { $_.PNPDeviceID -like 'USB\VID_303A*' -and $_.Name -match 'COM[0-9]+' } | ForEach-Object { $Matches[0] } | Select-Object -First 1"`) do set PORT=%%p
if "%PORT%"=="" (
  echo No ESP32-S3 on USB ^(VID 303A^). Connect it ^(docs\howto.md^), or give its port: flash.bat COM5
  pause
  exit /b 1
)
echo ESP32-S3 on %PORT%
esptool --chip esp32s3 -p %PORT% -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 80m 0x0 bootloader.bin 0x8000 partition-table.bin 0x10000 esp-spi.bin
pause
