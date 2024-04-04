sudo systemctl stop data-logger
sudo systemctl disable data-logger
sudo systemctl daemon-reload
sudo cp datalogger/data-logger.service /etc/systemd/system/data-logger.service
sudo systemctl start data-logger
sudo systemctl enable data-logger
sudo systemctl status data-logger
