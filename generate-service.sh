#!/bin/bash

# not root user
user=
while getopts "u" opt; do
	case "$opt" in
		u)
		UU=$SUDO_USER
		[  $UU ] || UU=$USER
		userfile='@'$UU
		usertext='User=%i'
		;;
	esac
done

shift $((OPTIND-1))

name=$1

[ $name ] || {
	echo "Error: Arg 1 shall be the program file"
	exit 1
}

bname=$(basename $name)
fullname=$(realpath $name)
[ -f $fullname ] || {
	echo "File does not exist"
	exit 1
}
servicename=$bname$userfile.service

echo "Generating $servicename..."

echo "[Unit]
Description=$bname
After=network.target

[Service]
ExecStart=$fullname
$usertext

[Install]
WantedBy=multi-user.target

" > $servicename

echo "Done."
echo "You must move it manually
  sudo cp $servicename /etc/systemd/system/"
echo "then enable it with
  sudo systemctl enable $servicename"


