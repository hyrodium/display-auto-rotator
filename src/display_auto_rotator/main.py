import serial
import subprocess
import time
import os


def main():
    ser = serial.Serial("/dev/ttyACM0", 115200)
    env = os.environ.copy()
    # env["DISPLAY"] = ":0"

    while True:
        line = ser.readline().decode().strip()
        print("line:", line)
        if line == "x-plus":
            subprocess.run(["xrandr", "--output", "DP-0", "--rotate", "normal"], env=env)
        if line == "y-plus":
            subprocess.run(["xrandr", "--output", "DP-0", "--rotate", "right"], env=env)
        time.sleep(0.1)
