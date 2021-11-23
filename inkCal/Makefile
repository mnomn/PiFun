# Installs service in "pi" users home directory.
# Systemd file can be used to start/stop/autostart service

name = inkCal
prog = $(name).py
systemd-service = $(name).service
target-dir=/home/pi/bin

.PHONY: install_pi

# Default values for remote system
# Set environment variables or add to commandline:
# "make REMOTE_HOST=pi@192.168.1.182 install_rpi"
REMOTE_HOST ?= pi@zerow.local

install_rpi:
	$(info "REMOTE_HOST: $(REMOTE_HOST)" )
	scp $(prog) $(REMOTE_HOST):$(target-dir)/$(prog)

	# First copy to home folder, because of write rights
	scp $(systemd-service) $(REMOTE_HOST):
	# Copy to correct place as sudo
	ssh $(REMOTE_HOST) "sudo cp $(systemd-service) /etc/systemd/system"
