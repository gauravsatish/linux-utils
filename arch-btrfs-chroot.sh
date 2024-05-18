sudo mkdir -p /mnt/boot/efi
sudo mount /dev/sda1 /mnt/boot/efi
sudo mount -o subvol=@ /dev/sda5 /mnt
sudo mount -o subvol=@cache /dev/sda5 /mnt/var/cache
sudo mount -o subvol=@log /dev/sda5 /mnt/var/log
sudo mount -o subvol=@home /dev/sda5 /mnt/home
sudo arch-chroot /mnt

