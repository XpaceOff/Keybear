
Here are the *.step files I import into plasticity to then create the case.

The first time I did this, I can export the STEP file from Kicad directly
but last time I tried I had many issues with the format. If that fails then
you could use Freecad to export the STEP file. 

Here are the two ways to export the STEP file:

## From Kicad directly
Go to `File` > `Export` > `STEP...` and select this directory

## From Freecad
- Install Freecad.
- Install the plugin called `StepUp Workbench`. In Freecad go to `Tools` > `Addon Manager` and install it.
- Restart Freecad.
- Open the `*.kicad_pcb` file from Freecad.
- Select the PCB and export the STEP file by going to `File` > `Export...`.
When ask about export options make sure to set:
    - Units for export of STEP: Millimeter
    - Export single object placement.
