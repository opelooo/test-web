mkdir -p /mnt/nfs_share
mount -t nfs 192.168.100.28:/srv/nfs_share /mnt/nfs_share

echo -e "192.168.100.28:/srv/nfs_share /mnt/nfs_share nfs defaults,bg 0 0" | sudo tee -a /etc/fstab
