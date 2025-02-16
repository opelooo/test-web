echo -e "\nacl my_private_net src 192.168.100.16/28\nhttp_access allow my_private_net" | sudo tee -a /etc/squid/squid.conf

sudo squid -k check
sudo systemctl restart squid
sudo systemctl status squid
