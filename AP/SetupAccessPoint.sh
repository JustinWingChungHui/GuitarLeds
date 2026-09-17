sudo nmcli connection add type wifi ifname wlan0 con-name Hotspot \
  ssid "MyPiAP" \
  802-11-wireless.mode ap \
  802-11-wireless.band bg \
  ipv4.method shared

sudo nmcli connection modify Hotspot \
  wifi-sec.key-mgmt wpa-psk \
  wifi-sec.psk "yourpassword" \
  wifi-sec.proto rsn \
  wifi-sec.pairwise ccmp

sudo nmcli connection up Hotspot

# Disable other saved wifi coonections
nmcli connection show
sudo nmcli connection modify "OtherProfileName" connection.autoconnect no


# Reboot
# Connect the WLED to the AP

# Find the MAC and IP address of the WLED controller
cat /var/lib/NetworkManager/dnsmasq-wlan0.leases

# Fix IP address of Wled controllers
sudo mkdir -p /etc/NetworkManager/dnsmasq-shared.d
sudo nano /etc/NetworkManager/dnsmasq-shared.d/reservations.conf

# Add a line like:
# dhcp-host=aa:bb:cc:dd:ee:ff,10.42.0.50


# Make the python script run on boot
sudo nano /etc/systemd/system/wled-button.service

# [Unit]
# Description=WLED Playlist Button Listener
# After=network.target

# [Service]
# ExecStart=/usr/bin/python3 /home/justin/monitor_pin.py
# Restart=always
# User=justin

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