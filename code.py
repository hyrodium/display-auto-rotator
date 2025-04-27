from math import atan2
import board
import analogio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Analog inputs
adc_x = analogio.AnalogIn(board.A0)  # GPIO 26
adc_y = analogio.AnalogIn(board.A1)  # GPIO 27

# HID keyboard config
kbd = Keyboard(usb_hid.devices)

# Initial status
t = 0.01
threshold_rot = 0.05


# ADC to read 16bit (0-65535)
def read_adc(adc):
    return adc.value


def load_xy():
    x = (adc_x.value - 32768) / 32768
    y = (adc_y.value - 32768) / 32768
    return x, y


def initialize_xy():
    x = 0.0
    y = 0.0
    n = 10
    for _ in range(n):
        _x, _y = load_xy()
        x += _x / n
        y += _y / n
    return x, y


status = 0
x, y = initialize_xy()

while True:
    _x, _y = load_xy()
    x = x * (1 - t) + _x * t
    y = y * (1 - t) + _y * t
    rot = atan2(y, x) / 6.2831853
    print(rot)

    if -threshold_rot < rot < threshold_rot:
        if status != 1:
            # Meta+Ctrl+PgUp (normal)
            kbd.press(Keycode.GUI, Keycode.CONTROL, Keycode.PAGE_UP)
            kbd.release_all()
            status = 1

    elif 0.25 - threshold_rot < rot < 0.25 + threshold_rot:
        if status != 2:
            # Meta+Ctrl+End (right)
            kbd.press(Keycode.GUI, Keycode.CONTROL, Keycode.END)
            kbd.release_all()
            status = 2

    elif rot < -0.5 + threshold_rot or rot > 0.5 - threshold_rot:
        if status != 3:
            # Do nothing (180° rotation is not allowed)
            status = 3

    elif -0.25 - threshold_rot < rot < -0.25 + threshold_rot:
        if status != 4:
            # Meta+Ctrl+HOME (left)
            kbd.press(Keycode.GUI, Keycode.CONTROL, Keycode.HOME)
            kbd.release_all()
            status = 4
