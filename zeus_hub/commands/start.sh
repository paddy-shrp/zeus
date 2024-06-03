cd /Users/patr/Documents/GitHub/zeus
sudo cp zeus_hub/zeus_hub.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tapit
sudo systemctl start tapit