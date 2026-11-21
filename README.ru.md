# Karabas Go, Mini, Mini G

[English](README.md) | Русский

Платы на ПЛИС Spartan-6 для эмуляции разных ретрокомпьютеров: Karabas Go и Karabas Mini /
Mini G. В этом репозитории лежит всё, что записывается на SD-карту и в платы (ядра, прошивка),
аппаратная документация (схемы, BOM, гербер-файлы) и 3D-модели корпусов всех плат. (У Mini раньше
был свой репозиторий, [karabas-mini](https://github.com/andykarpov/karabas-mini), теперь он в архиве.)

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

Схемотехника и документация распространяются по лицензии [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](http://creativecommons.org/licenses/by-nc-sa/4.0/).

Ядра ПЛИС, прошивка и прочие программные части распространяются по своим собственным лицензиям.

## С чего начать

[docs/howto.md](docs/howto.md) (на английском): ядра из `cores/` копируются в корень SD-карты 1
(один файл `.kg` на ядро для всех плат), прошивка платы берётся из `firmware/`:

| Плата | Прошивка |
| --- | --- |
| Karabas Go | `firmware/karabas_go.uf2` |
| Karabas Mini, rev.C .. rev.F3 | `firmware/karabas_mini.uf2` |
| Karabas Mini G, rev.G / G2 | `firmware/karabas_minig.uf2` |

Ядрам `.kg` нужна прошивка 26110415 или новее; старая прошивка останавливается с сообщением
"Boot file not found".

[Karabas Flasher](https://github.com/xdemax/kgff) (kgff, автор xdemax, MIT; Windows, Linux, macOS)
делает всё это в одном окне: скачивает прошивку и ядра из этого репозитория, прошивает RP2040,
заменяет ядра `.kg` на SD-карте 1 (старые переносятся в резервную папку), копирует дополнительный
контент (ROM-ы, образы дисков) и определяет модель платы командой `AT+KARABAS=version`.
Для обновления ядер нужна прошивка от 18.10.2026 или новее: если не уверены, сначала обновите
только прошивку.

### esxDOS 0.9.0 на SD-карте 2

В ядрах Karabas Pro (Profi) и ZX-Uno начиная со сборки 26112002 ПЗУ DivMMC —
[esxDOS 0.9.0](https://www.esxdos.org/). Эта ПЗУ проверяет версию `SYS/ESXDOS.SYS` и не стартует с
системными файлами 0.8.x, поэтому SD-карту 2 нужно обновить вместе с этими ядрами:

- скопируйте папки `SYS` и `BIN` из [esxdos090.zip](https://www.esxdos.org/files/esxdos090.zip)
  в корень SD-карты 2 (системные команды теперь лежат в `SYS/BIN`, их старые копии в `BIN`
  больше не используются);
- длинные имена файлов: возьмите новый `SYS/CONFIG/ESXDOS.CFG` или добавьте в свой строку `LFN=1`;
- ZX Next на той же карте: замените `machines/next/ESXMMC.BIN` на `ROMS/esxdos-0.9.0-divmmc.bin`
  из архива, переименовав его в `ESXMMC.BIN` (машинам Next с DivMMC нужна та же версия, что и
  в `SYS`);
- `NMI.SYS` / `RTC.SYS`, сделанные для старых версий esxDOS, нужно пересобрать под новые адреса
  ($2000 / $2F00). Для [Long Filename Browser](https://spectrumcomputing.co.uk/forums/viewtopic.php?f=9&t=2553)
  от Bob Fossil (`.browse`, `BROWSE.BIN` 1.01) есть обновлённый `NMI.SYS` от автора:
  [software/esxdos/NMI.SYS](software/esxdos/NMI.SYS), скопируйте его в `SYS` SD-карты 2 (проверено
  на Mini G с Profi и ZX-Uno);
- часы: [software/esxdos/RTC.SYS](software/esxdos/RTC.SYS) — RTC.SYS от ZX Next (DS1307 на I2C-портах
  103B / 113B), перенесённый на адрес $2F00 для 0.9.0; скопируйте его в `SYS` SD-карты 2. Работает с
  ядрами Karabas Pro (Profi) 26112103 / ZX-Uno 26112102 и новее (в них есть эти порты); со старым
  ядром `.date` выдаёт ошибку, без `RTC.SYS` — «No SYS»;
- сама ПЗУ лежит в файлах `.kg`: прошивать её лентами `FLASHERS` из архива не нужно.

## Содержимое

| Путь | Что там |
| --- | --- |
| `cores/` | ядра, `*.kg` (один файл для всех плат) |
| `firmware/` | прошивка RP2040 для каждой платы; `esp32-s3/` — прошивка ESP32-S3 шилда Mini G |
| `software/` | дополнительные файлы для ядер (`TBBLUE.FW` для ZX Next, `esxdos/NMI.SYS` браузера Bob Fossil, `esxdos/RTC.SYS`, плагины) |
| `docs/go/`, `docs/mini/` | схемы (PDF), интерактивные BOM, рендеры; `docs/mini/revF_mod.md` — доработка тактирования FT812 на Mini rev.C, D, F; `docs/mini/revG2_mod.md` — доработка ~CS SDRAM на rev.G2 |
| `pcb/go/`, `pcb/mini/` | гербер-файлы каждой ревизии, `PCB_CHANGELOG.md` |
| `case/go/`, `case/mini/` | 3D-модели корпусов |

## Платы

### Karabas Go

- ПЛИС Spartan-6 на 25k LE
- Микроконтроллер RP2040
- 4 порта USB
- 2 микросхемы SRAM по 2 МБ, 10 нс
- SDRAM 32 МБ
- Выход VGA 8:8:8
- Видеопроцессор FT812 на плате
- 16-битный аудио-ЦАП
- MIDI-синтезатор SAM2695
- 2 порта джойстика DB9, совместимых с Sega / Atari
- CF-карта
- 2 карты microSD
- Магнитофонный вход / выход
- Порт дисковода (FDD)
- Пищалка
- Часы реального времени DS3221
- EEPROM 1 КБ
- Модуль Wi-Fi ESP8266

Последняя ревизия платы — Rev.B4 ([список изменений](pcb/go/PCB_CHANGELOG.md)). Rev.B4 может
не совсем подходить к 3D-моделям корпусов: её карты microSD немного сдвинуты вперёд.
Исходники платы: [karabas-go-pcb](https://github.com/andykarpov/karabas-go-pcb).

![image](docs/go/karabas-go-top.png)

![image](docs/go/karabas-go-bot.png)

### Karabas Mini / Mini G

- ПЛИС Spartan-6 на 25k LE
- Микроконтроллер RP2040
- 4 порта USB
- 2 микросхемы SRAM по 2 МБ, 10 нс
- SDRAM 32 МБ
- Выход DVI
- Видеопроцессор FT812 на плате
- MIDI-синтезатор SAM2695
- 2 карты microSD
- Магнитофонный вход / выход
- Часы реального времени DS3221
- EEPROM 1 КБ
- Модуль Wi-Fi ESP8266
- Разъём расширения uBUS
- ESP32-S3 как микроконтроллер VDAC32
- CF-карта

Последняя стабильная ревизия платы — Rev.G ([список изменений](pcb/mini/PCB_CHANGELOG.md)).
Ревизиям C, D и F для ядер, использующих FT812, нужна небольшая [доработка](docs/mini/revF_mod.md). Ревизии G2 нужна
[доработка ~CS SDRAM](docs/mini/revG2_mod.md), без неё не работает ни одно ядро, использующее SDRAM.
Исходники платы: [karabas-mini-pcb](https://github.com/andykarpov/karabas-mini-pcb).

![image](docs/mini/karabas-mini-top.png)

![image](docs/mini/karabas-mini-bot.png)

Шилд с CF-картой и ESP32-S3 для rev.G (второй этаж):

![image](docs/mini/karabas-mini-shield-v4-top.png)

![image](docs/mini/karabas-mini-shield-v4-bot.png)

Шилд для шилда v4 с матричным дисплеем (третий этаж):

![image](docs/mini/karabas-mini-shield-v4-disp-top.png)

![image](docs/mini/karabas-mini-shield-v4-disp-bot.png)

## Исходники

Ядра ПЛИС:

- Загрузочное меню: https://github.com/andykarpov/karabas-go-core-menu
- Тестовое ядро: https://github.com/andykarpov/karabas-go-core-test
- TS-Conf: https://github.com/andykarpov/karabas-go-core-tsconf
- ZX Spectrum Next: https://github.com/andykarpov/karabas-go-core-next
- Karabas Pro: https://github.com/andykarpov/karabas-go-core-profi
- ZX-Uno (с General Sound и OPL3): https://github.com/andykarpov/karabas-go-core-zxuno
- PCXT: https://github.com/andykarpov/karabas-go-core-pcxt
- NES: https://github.com/andykarpov/karabas-go-core-nes
- SNES: https://github.com/andykarpov/karabas-go-core-snes
- Семейство Радио-86РК (РК86, Микроша, Апогей, Партнёр, Микро-80): https://github.com/andykarpov/karabas-go-core-rk
- Alf: https://github.com/andykarpov/karabas-go-core-alf
- MSX1: https://github.com/andykarpov/karabas-go-core-msx
- MSX2 / MSX2+: https://github.com/andykarpov/karabas-go-core-msx2
- ZX Evolution BaseConf: https://github.com/andykarpov/karabas-go-core-baseconf
- УКНЦ (МС-0511): https://github.com/andykarpov/karabas-go-core-uknc
- Орион-128: https://github.com/andykarpov/karabas-go-core-orion128
- Орион-ПРО: https://github.com/andykarpov/karabas-go-core-orionpro
- Специалист / Специалист-MX: https://github.com/andykarpov/karabas-go-core-specialist
- БК-0011М + AZBK: https://github.com/andykarpov/karabas-go-core-bk
- Atari ST / STE: https://github.com/andykarpov/karabas-go-core-atarist
- Sinclair QL: https://github.com/andykarpov/karabas-go-core-ql
- PDP-11/70 (форк tsybulin/karabas-go-core-pdp2026): https://github.com/andykarpov/karabas-go-core-pdp2026
- Commodore VIC-20: https://github.com/andykarpov/karabas-go-core-vic20
- Commodore 64: https://github.com/xdemax/karabas-go-core-c64
- Apple Macintosh Plus: https://github.com/andykarpov/karabas-go-core-macplus
- Apple //e: https://github.com/andykarpov/karabas-go-core-apple2
- Atari 2600 VCS: https://github.com/andykarpov/karabas-go-core-atari2600
- Atari 800XL: https://github.com/xdemax/karabas-go-core-atari800
- Amstrad CPC 464 / 664 / 6128: https://github.com/andykarpov/karabas-go-core-cpc
- BBC Micro Model B / Master 128: https://github.com/andykarpov/karabas-go-core-bbc
- Bandai WonderSwan / WonderSwan Color: https://github.com/andykarpov/karabas-go-core-wonderswan
- Agon Light / Console8: https://github.com/andykarpov/karabas-go-core-agon
- term (терминал xterm-256color: telnet / SSH через ESP8266, USB serial): https://github.com/andykarpov/karabas-go-core-term
- VT100 (терминал на USB-последовательном порту платы, getty на ПК): https://github.com/andykarpov/karabas-go-core-vt100
- RC2014 (Z80, RomWBW / CP/M, SCM, BASIC; терминал VT100 или TMS9918): https://github.com/andykarpov/karabas-go-core-rc2014
- V6Z80P+ (OSCA): https://github.com/Caasper911/karabas-go-core-v6z80p
- QuadSpeccy (четыре Pentagon 128 на одном экране): https://github.com/Caasper911/karabas-go-core-quadspeccy
- SpeccyWall / QuadSpeccyX4 (16 Pentagon 128 на одном экране, стена 4x4 в 1280x800): https://github.com/Caasper911/karabas-go-core-quadspeccyx4
- Uzebox (игровая консоль на ATmega644; игры .uze, SNES-джойстики, SD-карта или образ SD): https://github.com/Caasper911/karabas-go-core-uzebox
- КРИСС CP/M (criss.radio.ru; сеть через ESP8266): https://github.com/andykarpov/karabas-go-core-criss
- Gigatron TTL (TTL-микрокомпьютер Марселя ван Кервинка и Вальтера Белгерса; программы .gt1 с SD-карты): https://github.com/andykarpov/karabas-go-core-gigatron
- Вектор-06Ц (3 МГц с точными тактами ожидания, квазидиск, дискеты .fdd, AY, лента .wav; 576p с кадром оригинала): https://github.com/andykarpov/karabas-go-core-vector06c

Прошивка: https://github.com/andykarpov/karabas-go-firmware

Инструменты разработки (`make_core`): https://github.com/andykarpov/karabas-go-tools
