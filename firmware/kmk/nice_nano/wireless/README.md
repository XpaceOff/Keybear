# Keybear — nice!nano v2 Wireless Setup

This folder contains KMK firmware files for the Keybear keyboard using two **nice!nano v2** controllers with a **fully wireless BLE split** — no TRRS cable between halves. The keyboard connects to your PC over Bluetooth.

> **Status:** BLE split in KMK is functional but still described as "in testing" by the KMK project.  
> For a stable, battle-tested experience use the [wired setup](../wired/README.md) first.

---

## Requirements

- 2× nice!nano v2
- 2× LiPo / Li-Ion batteries (one per half) — the nice!nano has an onboard charging circuit
- CircuitPython **8.x or higher** (nRF52840 build)
- KMK firmware (must be **pre-compiled** — see below)
- `adafruit_ble` library

---

## Step 1 — Install CircuitPython on both halves

1. Download CircuitPython **8.2.6** for the nice!nano (the tested and recommended version):  
   https://adafruit-circuit-python.s3.amazonaws.com/bin/nice_nano/en_US/adafruit-circuitpython-nice_nano-en_US-8.2.6.uf2  
   *(Other versions are listed at https://circuitpython.org/board/nice_nano/ but 8.2.6 is known to work reliably with this setup.)*

2. Put the nice!nano into bootloader mode by **double-tapping the reset button**.  
   A drive called `NICENANO` appears.

3. Drag and drop the `.uf2` file onto the `NICENANO` drive.  
   The board reboots and a `CIRCUITPY` drive appears.

4. Repeat for the second half.

---

## Step 2 — Install the adafruit_ble library

BLE HID requires the Adafruit BLE library.

1. Download the **Adafruit CircuitPython Bundle** matching your CircuitPython version:  
   https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases

2. From the bundle, copy the `adafruit_ble/` folder to the `lib/` directory on **both** halves:
   ```
   KEYBEARL/
   └── lib/
       └── adafruit_ble/
   ```

---

## Step 3 — Rename the drives (required for auto-handedness)

KMK detects which half is left or right by reading the drive name. The left drive name must end in `L` and the right in `R`.

Open a serial console (e.g. Thonny, `screen`, or PuTTY) connected to each half and run:

```python
import storage
storage.remount("/", readonly=False)
import os
os.rename("/", "KEYBEARL")   # on the left half
# os.rename("/", "KEYBEARR") # on the right half
```

Or follow the official guide:  
https://learn.adafruit.com/welcome-to-circuitpython/renaming-circuitpy

---

## Step 4 — Pre-compile KMK (required for nice!nano)

The nice!nano has limited flash memory. KMK must be compiled to `.mpy` bytecode before copying.

### Option A — Download pre-compiled KMK

1. Go to: https://github.com/KMKfw/kmk_firmware/actions/workflows/compile.yml
2. Click the latest successful build.
3. Download the artifact ZIP at the bottom of the page.
4. Unzip it — you will get a `kmk/` directory with `.mpy` files.

### Option B — Compile KMK yourself

1. Download `mpy-cross` **8.2.6** matching your OS:
   - **Windows:** https://adafruit-circuit-python.s3.amazonaws.com/bin/mpy-cross/windows/mpy-cross-windows-8.2.6.static.exe
   - **Linux (x86-64):** https://adafruit-circuit-python.s3.amazonaws.com/bin/mpy-cross/linux-amd64/mpy-cross-linux-amd64-8.2.6.static

2. Add `mpy-cross` to your PATH:

   **Windows** — rename the file to `mpy-cross.exe` and move it to a folder already on your PATH (e.g. `C:\Windows\System32`), or add its folder to PATH via *System Properties → Environment Variables*.

   **Linux** — make the file executable, rename it, and add it to your PATH:
   ```sh
   # Make executable and rename
   chmod +x mpy-cross-linux-amd64-8.2.6.static
   mv mpy-cross-linux-amd64-8.2.6.static mpy-cross

   # Move to a directory already on PATH (e.g. /usr/local/bin)
   sudo mv mpy-cross /usr/local/bin/

   # Verify it works
   mpy-cross --version
   ```
   If you prefer not to use `sudo`, place it in `~/.local/bin/` instead and make sure that directory is on your PATH:
   ```sh
   mkdir -p ~/.local/bin
   mv mpy-cross ~/.local/bin/
   # Add to ~/.bashrc or ~/.zshrc if not already present:
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. In the KMK repo root, run:
   ```sh
   python util/compile.py
   ```
   The compiled `.mpy` files are written to a `build/` folder created inside the KMK repo (e.g. `kmk_firmware/build/kmk/`). Copy the `kmk/` folder from there — **not** the source `kmk/` folder at the repo root.

> **Tip — reduce flash usage:**  
> Only copy the KMK sub-modules you actually use.  
> The files imported by this config are:
> - `kmk/modules/layers.py`
> - `kmk/modules/holdtap.py`
> - `kmk/modules/split.py`
> - `kmk/modules/encoder.py`
> - `kmk/modules/cg_swap.py`
> - `kmk/modules/dynamic_sequences.py`
> - `kmk/modules/mouse_keys.py`
> - `kmk/extensions/rgb.py`
> - `kmk/extensions/lock_status.py`

---

## Step 5 — Copy files to each half

Copy the following to the **root** of both `KEYBEARL` and `KEYBEARR` drives:

```
KEYBEARL/  (and KEYBEARR/)
├── boot.py           ← from KMK repo root
├── kmk/              ← compiled KMK folder (from Step 4)
├── lib/
│   └── adafruit_ble/ ← from Step 2
├── kb.py             ← from this folder
└── code.py           ← from this folder
```

The `boot.py` is in the root of the KMK repository:  
https://github.com/KMKfw/kmk_firmware/blob/main/boot.py

---

## Step 6 — Pair with your PC

1. Power on both halves (connect batteries or USB-C for testing).

2. On your PC, open Bluetooth settings and scan for new devices.  
   You should see **"Keybear"** appear (the `ble_name` set in `code.py`).

3. Click to pair.

4. The two halves will connect to each other automatically using BLE split.  
   The half with the USB plug detected (or the one named `KEYBEARL`) acts as the BLE host.

> The keyboard advertises as `"Keybear"`. To change the name, edit the `ble_name` argument in `code.py`:
> ```python
> keyboard.go(hid_type=HIDModes.BLE, ble_name='Keybear')
> ```

---

## Battery wiring

The nice!nano v2 has a built-in LiPo charger. Connect the battery to the `BAT+` and `GND` pads on the underside of the board.

- The battery charges whenever USB is plugged in.
- To protect the battery when unused for long periods, disconnect it physically or add a power switch between `BAT+` and the board.

> **RGB and battery life:**  
> RGB LEDs consume significant power. The default brightness (`val_default`) in this config is set to `50` (out of 255).  
> For maximum battery life, reduce it further or disable RGB entirely by removing the `RGB` extension.

---

## Pin mapping reference

| Role | nice!nano pin | Pro Micro index |
|---|---|---|
| Column 0 | P0_31 | 19 |
| Column 1 | P0_29 | 18 |
| Column 2 | P0_02 | 17 |
| Column 3 | P1_15 | 16 |
| Column 4 | P1_13 | 15 |
| Column 5 | P1_11 | 14 |
| Row 0 | P0_22 | 6 |
| Row 1 | P0_24 | 7 |
| Row 2 | P1_00 | 8 |
| Row 3 | P0_11 | 9 |
| Encoder A | P1_04 | 10 |
| Encoder B | P1_06 | 11 |
| RGB data | P0_09 | 12 |

No UART data pins are needed — BLE is used for split communication.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `CIRCUITPY` fills up / import error | KMK was not pre-compiled. Repeat Step 4. |
| Keyboard not visible to PC | Ensure `adafruit_ble` is in `lib/`. Check drive names end in `L`/`R`. |
| Only one half works | Both halves must be powered. BLE split needs both sides running. |
| Wrong half is master | Rename drives so left ends in `L`, right in `R`. |
| Keyboard disconnects randomly | Check battery level. RGB at full brightness drains batteries quickly. |
| Need to re-pair | Delete the device from your OS Bluetooth settings, then power-cycle both halves and pair again. |

---

## Updating the keymap

Edit `code.py` on **both halves** (the keymap must be identical on each side).  
After saving, CircuitPython auto-reloads — no reflashing needed.  
You can connect via USB-C to either half for editing even in wireless mode.
