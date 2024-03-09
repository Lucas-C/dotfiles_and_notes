# Restore grub : boot with livecd and as root:
mount /dev/sda8 /mnt
#grub-install --root-directory=/mnt /dev/sda # only if Ubuntu versions differ between LiveCD & OS
for i in /dev /proc /sys; do mount --bind $i /mnt$i; done
chroot /mnt
grub-mkconfig && update-grub && grub-install /dev/sd... # the 1st & 3rd helped fix Simon's laptop
exit
for i in /mnt/dev /mnt/proc /mnt/sys /mnt; do umount $i; done
dd bs=512 count=1 if=/dev/sda 2>/dev/null | strings # check the MBR
reboot

sudo sed -i 's/enabled=1/enabled=0/' /etc/default/apport # Disable System Crash Reports

# Change desktop directory
~/.config/user-dirs.dirs # edit XDG_DESKTOP_DIR

~/.config/variety/variety.conf # wallpaper changer minor change: gsettings set org.cinnamon.background picture-options centered
# Alt, ran only once: gsettings set org.gnome.desktop.background picture-options centered
# Alt: wallch
