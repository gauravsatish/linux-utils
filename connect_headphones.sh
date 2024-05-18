#!/bin/bash

# Bluetooth device address
DEVICE_ADDR="E4:22:A5:BE:00:7F"

# Function to remove and re-pair the device
fresh_connect() {
  echo "Removing device $DEVICE_ADDR..."
  echo "remove $DEVICE_ADDR" | bluetoothctl

  echo "Starting scan..."
  echo "scan on" | bluetoothctl

  echo "Waiting for the device to appear..."
  while true; do
    if bluetoothctl devices | grep -q "$DEVICE_ADDR"; then
      echo "Device found, pairing..."
      echo "pair $DEVICE_ADDR" | bluetoothctl
      echo "connect $DEVICE_ADDR" | bluetoothctl
      echo "scan off" | bluetoothctl
      break
    fi
    sleep 1
  done
}

# Function to directly connect to the device
direct_connect() {
  echo "Connecting to device $DEVICE_ADDR..."
  echo "connect $DEVICE_ADDR" | bluetoothctl
}

# Check for arguments
if [[ "$1" == "-f" || "$1" == "--fresh" ]]; then
  fresh_connect
else
  direct_connect
fi
