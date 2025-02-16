echo -e "192.168.100.28:/srv/nfs_share /mnt/nfs_share nfs defaults,bg 0 0" | sudo tee -a /etc/fstab

nc -vz 192.168.100.28 2049
