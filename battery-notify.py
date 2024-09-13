#!/usr/bin/env python3
from enum import Enum
import subprocess
from time import sleep

state = None

class BatteryState(Enum):
    CHARGING = "Battery charging"
    DISCHARGING = "Battery discharging"
    NOTCHARGING = "Battery not charging"

def notify(result):
    global state
    if result != state:
        if result == "Charging":
            if state == "Not charging":
                return
            subprocess.run(["notify-send", "Battery Update", BatteryState.CHARGING.value])
        elif result == "Discharging":
            subprocess.run(["notify-send", "-u", "critical", "Battery Update", BatteryState.DISCHARGING.value])
        elif result == "Not charging":
            subprocess.run(["notify-send", "Battery Update", BatteryState.NOTCHARGING.value])
        state = result

while True:
    result = subprocess.run(["cat", "/sys/class/power_supply/BAT0/status"], capture_output=True, text=True)
    notify(result.stdout.strip())
    sleep(10)
