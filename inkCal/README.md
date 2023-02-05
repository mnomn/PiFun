# Ink Calender

Script for Rasperry Pi and Pimoroni Inky pHAT.

Displays the date, week number and weather forcast.

## How it works

A systemd service starts a python script.

The python script fetch weather forecast, then prints the weather and date on the display.

## Install

- InkyPhat python library has to be installed on the pi.
- Rename inkCal.json.template to inkCal.json and set correct vales.
- Install with make install_rpi
- Enable systemd (from ssh terminal) "sudo systemctl enable inkCal"

## Icons

Not included in this git.
Create a folder "icon" and download pngs from openweathermap.org

Comes from  https://openweathermap.org/weather-conditions

Download:
`curl http://openweathermap.org/img/wn/10d.png -o 10d.png`

## Todo?

- draw wether icons
- ~~Caclulate week~~
- ~~Get weather forcast?~~
- Get calendar?
- Automatic find location for weather?
- ~~Settings city for weather, screen orientation, etc~~
- Set weekday and month names in config json
