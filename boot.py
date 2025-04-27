import usb_cdc
import storage

# Disable USB storage and CDC
usb_cdc.disable()
storage.disable_usb_drive()
