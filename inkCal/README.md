# Ink Calender

Script for Rasperry pi and pimoroni inkyphat.

Displays the date, week number and weather forcast.

## How it works

A systemd service starts a python script.

The python script fetch weather, then prints the weather and date on the display.

## Install

- InkyPhat python library has to be installed on the pi.
- Rename inkCal.json.template to inkCal.json.template and set correct vales.
- Install with make install_rpi
- Enable systemd (from ssh terminal) "sudo systemctl enable inkCal"

## Todo

Caclulate week
Get weather forcast?
Get calendar?
Automatic find location for weather?
Settings city for weather, screen orientation, etc
Use POST API? Use a settings file?
