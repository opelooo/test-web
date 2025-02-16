sudo dnf install -y nfs-utils nfs-server firewalld

sudo systemctl enable --now rpcbind
sudo systemctl enable --now nfs-server

sudo mkdir -p /srv/nfs_share
sudo chown -R nobody:nobody /srv/nfs_share
sudo chmod 755 /srv/nfs_share

echo -e "/srv/nfs_share  *(rw,sync,no_root_squash)" | sudo tee -a /etc/exports

sudo exportfs -rav
sudo exportfs -a
sudo systemctl start nfs-server
sudo systemctl enable nfs-server
sudo systemctl start rpcbind
sudo systemctl enable rpcbind

sudo systemctl start firewalld
sudo firewall-cmd --permanent --add-port=2049/tcp
sudo firewall-cmd --permanent --add-port=2049/udp
sudo firewall-cmd --permanent --add-port=111/tcp
sudo firewall-cmd --permanent --add-port=111/udp
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
