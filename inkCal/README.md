# Ink Calender

Script for Rasperry pi and pimoroni inkyphat.

Displays the date, week number and weather forcast.

## How it works

A systemd service starts a python script.

The python script fetch weather, then prints the weather and date on the display.

InkyPhat python library has to be installed on the pi.

## Todo

Caclulate week
Get weather forcast?
Get calendar?
Automatic find location for weather?
Settings city for weather, screen orientation, etc
Use POST API? Use a settings file?
