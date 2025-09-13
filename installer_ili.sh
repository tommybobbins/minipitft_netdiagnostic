#!/bin/bash
sudo apt update -y
sudo apt-get update -y
sudo apt-get upgrade -y
sudo rpi-update 
cd ~
sudo pip3 install --upgrade adafruit-python-shell click
sudo apt-get install -y git
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts
sudo apt-get install python3-pip python3-click -y
sudo pip3 install adafruit-circuitpython-rgb-display --break-system-packages
sudo pip3 install --upgrade --force-reinstall spidev --break-system-packages
sudo pip3 install adafruit-circuitpython-ili9341 --break-system-packages
sudo pip3 install displayio --break-system-packages --break-system-packages

sudo apt-get install fonts-dejavu python3-pil python3-numpy -y
cd ~/minipitft_netdiagnostic
echo <<EOF >>~/.bashrc
if [ $XDG_VTNR ]
then
  /usr/local/bin/netdiag.py > ~/netdiag_output.log
fi
EOF
cp -p netdiag_ili.py /usr/local/bin/netdiag.py
sudo reboot
