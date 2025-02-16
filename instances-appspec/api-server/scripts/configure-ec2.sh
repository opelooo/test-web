
sudo dnf update -y
sudo dnf install -y mariadb105 firewalld python3-pip
sudo systemctl start firewalld
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
