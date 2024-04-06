sudo systemctl stop data_logger
sudo systemctl disable data_logger
sudo systemctl daemon-reload
sudo cp datalogger/data_logger.service /etc/systemd/system/data_logger.service
sudo systemctl start data_logger
sudo systemctl enable data_logger
sudo systemctl status data_logger
