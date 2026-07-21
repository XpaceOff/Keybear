import storage
import usb_cdc
import usb_hid

# 1. Keep the data/serial pipeline active so KMK can communicate
usb_cdc.enable(console=True, data=True)

# 2. Safely disable the mass storage USB drive 
storage.disable_usb_drive()

# 3. Formally re-map the hardware endpoints strictly to Keyboard
usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE))
