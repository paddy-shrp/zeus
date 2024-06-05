cd ~/Documents/GitHub/zeus

sudo cp zeus_hub/zeus_hub.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable zeus_hub
sudo systemctl start zeus_hub