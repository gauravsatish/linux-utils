#!/usr/bin/env python3
from enum import Enum
import subprocess
from time import sleep

state = None
lastid = None
dischargecount = 0

class BatteryState(Enum):
    CHARGING = "Battery charging"
    DISCHARGING = "Battery discharging"
    NOTCHARGING = "Battery not charging"

def convert_enum(status):
    if status == "Charging":
        return BatteryState.CHARGING
    elif status == "Discharging":
        return BatteryState.DISCHARGING
    elif status == "Not charging":
        return BatteryState.NOTCHARGING

def send_notification(args):
    global lastid
    if lastid is None:
        id = subprocess.run(["notify-send", "-p"] + args, capture_output=True, text=True)
    else:
        id = subprocess.run(["notify-send", "-p", "-r", lastid] + args, capture_output=True, text=True)
    lastid = id.stdout.strip()

def notify(result):
    global state
    global dischargecount
    if result != state:
        if state == BatteryState.DISCHARGING: dischargecount = 0
        if result == BatteryState.CHARGING:
            if state == BatteryState.NOTCHARGING:
                return
            send_notification(["Battery Update", BatteryState.CHARGING.value])
        elif result == BatteryState.DISCHARGING:
            send_notification(["-u", "critical", "Battery Update", BatteryState.DISCHARGING.value])
        elif result == BatteryState.NOTCHARGING:
            if state == BatteryState.CHARGING:
                return
            send_notification(["Battery Update", BatteryState.NOTCHARGING.value])
        state = result
    else:
        if state == BatteryState.DISCHARGING:
            dischargecount += 1
            if dischargecount % 6 == 0:
                send_notification(["-u", "critical", "Battery Update", BatteryState.DISCHARGING.value])

while True:
    result = subprocess.run(["cat", "/sys/class/power_supply/BAT0/status"], capture_output=True, text=True)
    notify(convert_enum(result.stdout.strip()))

    sleep(10)
