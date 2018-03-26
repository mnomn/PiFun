#!/bin/bash

name=bless-you
filename=$name.service

echo "Generating $filename..."

echo "[Unit]
Description=ble scanner, sends data to mqtt or http
After=network.target

[Service]
ExecStart=$PWD/$name

[Install]
WantedBy=multi-user.target

" > $filename

echo "Done.
You must move it manually
sudo cp $name /etc/systemd/system/
then enable it with
sudo systemctl enable $name
"

