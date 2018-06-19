#!/bin/bash

name=$1

[ $name ] || {
	echo "Error: Arg 1 shall be the program file"
	exit 1
}

bname=$(basename $name)
fullname=$(realpath $name)
servicename=$bname.service

echo "Generating $servicename..."

echo "[Unit]
Description=$bname
After=network.target

[Service]
ExecStart=$fullname

[Install]
WantedBy=multi-user.target

" > $servicename

echo "Done."
echo "You must move it manually
  sudo cp $servicename /etc/systemd/system/"
echo "then enable it with 
  sudo systemctl enable $bname"


