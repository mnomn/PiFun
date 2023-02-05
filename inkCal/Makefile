# Installs service in "pi" users home directory.
# Systemd file can be used to start/stop/autostart service

name = inkCal
prog = $(name).py
config = $(name).json
systemd-service = $(name).service

target_files = $(systemd-service) $(name).py $(name).json arguments.py settings.py weather.py
icon_files = icons
target-dir=/home/pi/inkCal

.PHONY: install_rpi

# Default values for remote system
# Set environment variables or add to commandline:
# "make REMOTE_HOST=pi@192.168.1.182 install_rpi"
REMOTE_HOST ?= pi@zerow.local

install_rpi:
	$(info "REMOTE_HOST: $(REMOTE_HOST)" )
	ssh $(REMOTE_HOST) "mkdir -p  $(target-dir)"
	scp $(target_files) $(REMOTE_HOST):$(target-dir)/

	# Copy systemd to correct place as sudo
	ssh $(REMOTE_HOST) "sudo cp $(target-dir)/$(systemd-service) /etc/systemd/system"

install_rpi_icons:
	$(info "Local icon dir: $(icon_files)" )
	$(info "Remote icon dir: $(REMOTE_HOST):$(target-dir)" )
	ssh $(REMOTE_HOST) "mkdir -p  $(target-dir)"
	scp -r $(icon_files) $(REMOTE_HOST):$(target-dir)/
