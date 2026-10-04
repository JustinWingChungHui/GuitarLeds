# Download from https://armbian.com/boards/bananapim2zero
# Debian 13 (Minimal CLI)

# Before installing, open sdcard and edit /etc/modules
# Put # to front of g_serial in the first line and save.
# This will allow keyboard to work

# Run the updates
sudo apt update

# Crashes on reboot
# sudo apt upgrade 

sudo apt autoremove

# Setup Python and dependencies
sudo apt install build-essential git python3 python3-dev python-is-python3 python3-requests python3-setuptools

# System files for the B-Pi M2 Zero
git clone https://github.com/CTXz/bpi-m2z-system-files.git
cd bpi-m2z-system-files
chmod +x install.sh
sudo ./install.sh
cd ..

# Setup wiringPi
git clone https://github.com/bontango/BPI-WiringPi2
cd BPI-WiringPi2
chmod +x build
sudo ./build

curl -s https://raw.githubusercontent.com/TuryRx/Bananapi-m2-zero-GPIO-files/master/gpioread.sh | sudo tee /usr/local/bin/gpioread > /dev/null
sudo chmod o+x /usr/local/bin/gpioread
sudo chmod 777 /usr/local/bin/gpioread
sudo touch /var/lib/bananapi/gpio
sudo chmod o+x /var/lib/bananapi/gpio
sudo chmod 777 /var/lib/bananapi/gpio
#To test out wiringPi, you may now use the gpio readall command


# RPi.GPIO
git clone https://github.com/GrazerComputerClub/RPi.GPIO.git
cd RPi.GPIO
sudo CFLAGS="-fcommon -Wno-error=implicit-function-declaration" python3 setup.py install


# Set up Access Point
sudo apt install dnsmasq-base
sudo apt-get install network-manager

# Hand wlan0 over to NetworkManager
sudo nano /etc/NetworkManager/NetworkManager.conf
# set managed=true

# Add home wifi connection
sudo nmcli connection add type wifi ifname wlan0 con-name wlan0-SsidName ssid "SSID" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "Password"

sudo nano /etc/netplan/*.yaml
# change renderer: networkd to renderer: NetworkManager
sudo netplan apply

sudo systemctl disable --now systemd-networkd

# reboot the system to apply changes
sudo reboot

sudo nmcli connection add type wifi ifname wlan0 con-name Hotspot ssid "MyAP" 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared

sudo nmcli connection modify Hotspot wifi-sec.key-mgmt wpa-psk wifi-sec.psk "MyPassword" wifi-sec.proto rsn wifi-sec.pairwise ccmp

# Had to run this command to get my android phone to connect to it.  Not sure if it's necessary for all devices.
sudo nmcli connection modify "Hotspot" 802-11-wireless-security.pmf 1

sudo nmcli connection up Hotspot

# Disable other saved wifi coonections
nmcli connection show
sudo nmcli connection modify "OtherProfileNames" connection.autoconnect no


# Reboot
# Connect the WLED to the AP

# Find the MAC and IP address of the WLED controller
sudo cat /var/lib/NetworkManager/dnsmasq-wlan0.leases

# Fix IP address of Wled controllers
sudo mkdir -p /etc/NetworkManager/dnsmasq-shared.d
sudo nano /etc/NetworkManager/dnsmasq-shared.d/reservations.conf

# Add a line like:
# dhcp-host=d4:e9:f4:fa:7e:08,10.42.0.142
# dhcp-host=1c:c3:ab:bf:34:e4,10.42.0.13 


# Make the python script run on boot
sudo nano /etc/systemd/system/wled-button.service

# [Unit]
# Description=WLED Playlist Button Listener
# After=network.target

# [Service]
# ExecStart=/usr/bin/python3 /home/justin/monitor_pin.py
# Restart=always
# User=root

# [Install]
# WantedBy=multi-user.target

# Double-check the path to python3:
which python3
# If it's not /usr/bin/python3, update ExecStart to match.

sudo systemctl daemon-reload
sudo systemctl enable wled-button.service
sudo systemctl start wled-button.service

# Verify it's running
sudo systemctl status wled-button.service

# stop the service if needed
sudo systemctl stop wled-button.service