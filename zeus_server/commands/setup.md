
### Basic Server Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo adduser zeus
sudo usermod -aG sudo zeus
sudo rsync --archive --chown=zeus:zeus ~/.ssh /home/zeus
```

Change the config file
```bash
sudo nano /etc/ssh/sshd_config
Port 2200
PermitRootLogin no 
AllowUsers root
```

```bash
sudo systemctl restart sshd
sudo ufw allow OpenSSH
sudo ufw enable
```

### Setup Nginx

```bash
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```