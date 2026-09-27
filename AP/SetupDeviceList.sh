# Make the python script run on boot
sudo nano /etc/systemd/system/device_list_server.service

# Double-check the path to python3:
which python3
# If it's not /usr/bin/python3, update ExecStart to match.

sudo systemctl daemon-reload
sudo systemctl enable device_list_server.service
sudo systemctl start device_list_server.service

# Verify it's running
sudo systemctl status device_list_server.service

# stop the service if needed
sudo systemctl stop device_list_server.service