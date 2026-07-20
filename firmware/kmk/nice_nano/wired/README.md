# Keybear — nice!nano v2 Wired Setup

This folder contains KMK firmware files for the Keybear keyboard using two **nice!nano v2** controllers connected via a **USB cable** (wired UART split). This is a custom feature of the Keybear PCB design — the inter-half USB connector replaces the TRRS jack found on most split keyboards. The keyboard connects to your PC over USB-C.

---

## Requirements

- 2× nice!nano v2
- 1× USB cable for the split connection between the two halves (custom PCB connector)
- CircuitPython **8.x or higher** (nRF52840 build)
- KMK firmware (must be **pre-compiled** — see below)
- USB-C cable (to connect left half to PC)

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

## Step 2 — Rename the drives (required for auto-handedness)

KMK detects which half is left or right by reading the drive name. The left drive name must end in `L` and the right in `R`.

With the nice!nano connected via USB, the `CIRCUITPY` drive will appear in your file manager. Rename it directly from your OS:

- **Windows:** right-click the drive in Explorer → **Rename** → type `KEYBEAR_L` (left) or `KEYBEAR_R` (right).
- **macOS:** click the drive on the Desktop or in Finder → press **Return** → type the new name.
- **Linux:** rename via your file manager or with `mlabel` / `udisksctl`.

Repeat for the second half with the opposite name.

---

## Step 3 — Pre-compile KMK (required for nice!nano)

The nice!nano has limited flash memory. KMK must be compiled to `.mpy` bytecode before copying.

### Option A — Download pre-compiled KMK

1. Go to: https://github.com/KMKfw/kmk_firmware/actions/workflows/compile.yml
2. Click the latest successful build.
3. Download the artifact ZIP at the bottom of the page.
4. Unzip it — you will get a `kmk/` directory containing `.mpy` files.

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
   The compiled `.mpy` files are written to a `build/` folder created inside the KMK repo (e.g. `kmk_firmware/build/kmk/`).

> **Tip — reduce flash usage further:**  
> Only copy the KMK sub-modules you actually use.  
> Skip the contents of `kmk/extensions/` and `kmk/modules/` that are not imported in `code.py`.  
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

## Step 4 — Compile the custom neopixel driver

This firmware uses a custom minimal `neopixel.py` (found in this folder) instead of the full Adafruit library, which saves significant flash space. It must be compiled to `.mpy` before copying.

From this folder, run:

```sh
mpy-cross neopixel.py
```

This produces `neopixel.mpy` in the same folder. Copy **only** the `.mpy` file to the board (not the `.py` source).

---

## Step 5 — Copy files to each half

Copy the following to the **root** of both `KEYBEARL` and `KEYBEARR` drives:

```
KEYBEARL/  (and KEYBEARR/)
├── boot.py        ← from KMK repo root
├── kmk/           ← compiled KMK folder in `build/` (from Step 3)
├── neopixel.mpy   ← compiled in Step 4
├── kb.py          ← from this folder
└── code.py        ← from this folder
```

The `boot.py` file is found in the root of the KMK repository:  
https://github.com/KMKfw/kmk_firmware/blob/main/boot.py

---

## Step 6 — Connect the split cable and plug in USB

1. Connect the USB cable between the two halves using the inter-half connector on the PCB.

2. Plug the USB-C cable into the **left half** (the split target).

3. The keyboard should be recognised immediately as a USB HID device.

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
| UART RX | RX | 1 |
| UART TX | TX | 0 |

These indices match the `nice_nano` quickpin table in KMK:  
`kmk/quickpin/pro_micro/nice_nano.py`

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `CIRCUITPY` fills up / import error | KMK was not pre-compiled. Repeat Step 3. |
| `neopixel` import error | `neopixel.mpy` is missing. Repeat Step 4 and copy it to the drive. |
| Only one half works | Check the inter-half USB cable is seated. Plug the PC cable into the **left** half. |
| Wrong half is master | Rename drives so left ends in `L`, right in `R`. |
| Keys wrong side | Swap the drive names (`L`/`R`). |
| Keyboard not detected | Check `boot.py` is present at root of the drive. |

---

## Updating the keymap

Edit `code.py` on **both halves** (the keymap must be identical on each side).  
After saving, CircuitPython auto-reloads — no reflashing needed.
