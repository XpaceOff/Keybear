I downloaded Ergogen in a folder called `tmp` in the upper directory.

projects
  |-- tmp
  | |-- ergogen
  |-- Keybear

to compile the Kicad files from the Ergogen config file I do:

```bash
cd Keybear

# For PCB
node ..\tmp\ergogen\src\cli.js keybear-chocolate\ergogen\ -o keybear-chocolate\ergogen\out\PCB

# For Plate
node ..\tmp\ergogen\src\cli.js keybear-chocolate\ergogen\ -o keybear-chocolate\ergogen\out\Plate
```

> [!Note] 
> To generate the plate you will need to change the value of `pcbs.keybear.outlines.main.outline`
> to `combo`. Generate the plate and remember to set it back to `plate`
