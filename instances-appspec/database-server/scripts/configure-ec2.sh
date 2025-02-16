sudo dnf update -y
sudo dnf install -y mariadb105 mariadb105-server firewalld
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo systemctl status mariadb

sudo systemctl start firewalld
sudo firewall-cmd --permanent --add-port=3306/tcp
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
