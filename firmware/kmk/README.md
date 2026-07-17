# Keybear KMK Firmware

This folder contains KMK firmware configurations for the Keybear keyboard.  
Each subfolder targets a specific microcontroller. The PCB and wiring are identical across all variants — only the controller and its pin names differ.

---

## PCB Pad Map

The pad numbers below refer to the physical pads on the Keybear PCB, following the standard Pro Micro pinout layout.

```
Pad 24 ── RAW              TX  ── Pad 1
Pad 23 ── GND              RX  ── Pad 2
Pad 22 ── RST              GND ── Pad 3
Pad 21 ── VCC              GND ── Pad 4
Pad 20 ── COL0             SDA ── Pad 5
Pad 19 ── COL1             SCL ── Pad 6
Pad 18 ── COL2             ROW0 ── Pad 7
Pad 17 ── COL3             ROW1 ── Pad 8
Pad 16 ── COL4             ROW2 ── Pad 9
Pad 15 ── COL5             ROW3 ── Pad 10
Pad 14 ── CS               ENCA ── Pad 11
Pad 13 ── LED              ENCB ── Pad 12
```

| Pad | Function | Notes |
|-----|----------|-------|
| 1   | TX       | UART transmit — split comms |
| 2   | RX       | UART receive — split comms |
| 3   | GND      | |
| 4   | GND      | |
| 5   | SDA      | I2C data |
| 6   | SCL      | I2C clock |
| 7   | ROW0     | Matrix row 0 |
| 8   | ROW1     | Matrix row 1 |
| 9   | ROW2     | Matrix row 2 |
| 10  | ROW3     | Matrix row 3 |
| 11  | ENCA     | Rotary encoder pin A |
| 12  | ENCB     | Rotary encoder pin B |
| 13  | LED      | RGB data line |
| 14  | CS       | |
| 15  | COL5     | Matrix column 5 |
| 16  | COL4     | Matrix column 4 |
| 17  | COL3     | Matrix column 3 |
| 18  | COL2     | Matrix column 2 |
| 19  | COL1     | Matrix column 1 |
| 20  | COL0     | Matrix column 0 |
| 21  | VCC      | 3.3 V power |
| 22  | RST      | Reset |
| 23  | GND      | |
| 24  | RAW      | Battery / unregulated power input |

---

## Controller Variants

| Folder | Controller | Split | BLE |
|--------|------------|-------|-----|
| [`blok/`](blok/) | Boardsource BLOK (RP2040) | Wired UART | No |
| [`nice_nano/wired/`](nice_nano/wired/) | nice!nano v2 (nRF52840) | Wired UART | No |
| [`nice_nano/wireless/`](nice_nano/wireless/) | nice!nano v2 (nRF52840) | BLE | Yes |
| [`nice_nano/wired/mix/`](nice_nano/wired/mix/) | nice!nano (left) + BLOK (right) | Wired UART | No |

---

## BLOK Setup

- Install CircuitPython [v8.2.6](https://adafruit-circuit-python.s3.amazonaws.com/bin/boardsource_blok/en_US/adafruit-circuitpython-boardsource_blok-en_US-8.2.6.uf2)
- Get a KMK copy of this [commit 5525233](https://github.com/KMKfw/kmk_firmware/archive/5525233cb957c367e4f0b589abcaeb1b5da53ec0.zip)

For nice!nano variants see the README inside the relevant subfolder.
