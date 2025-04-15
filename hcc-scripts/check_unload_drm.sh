#!/bin/bash
# use this script if irqs are occupied which cause pci_* to fail
sudo systemctl stop nvidia-persistenced
sudo rmmod nvidia_drm
sudo rmmod nvidia_modeset
