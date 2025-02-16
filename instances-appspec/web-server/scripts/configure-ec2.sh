sudo dnf update -y
sudo dnf install -y nginx nmap firewalld squid nfs-utils
sudo dnf install -y python3-pip

sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl enable squid
sudo systemctl start squid

sudo systemctl start firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
sudo firewall-cmd --list-all

sudo mv -f nginx/index.html /usr/share/nginx/html/index.html
sudo mv nginx/api.conf /etc/nginx/conf.d/api.conf
sudo mv nginx/web.conf /etc/nginx/conf.d/web.conf

sudo nginx -t
sudo systemctl restart nginx

