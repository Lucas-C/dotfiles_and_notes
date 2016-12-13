apt-get install aptitude
aptitude install vim tilda git svn screen tmux g++ openjdk-7-jdk vlc
aptitude install strace traceroute mtr
aptitude install nautilus-open-terminal scite grisbi texlive graphviz doxygen doxygen-gui libsdl-mixer1.2* mtpaint gaupol timidity-interfaces-extra timidity freepats most
sudo apt-get --purge remove tex.\*-doc$ # can save 700 MB of disk space
# Fix for tilda on maverick : echo "export TERM=xterm" | sudo tee /etc/profile.d/set_term.sh && source /etc/profile
# (Système>Préférence>Clavier->Agencements->Options de l'agencement : espace insecable à tout niveau SINON pbs avec barre espace)
aptitude install tkcon libsdl1.2debian-all libaudiere-1.9.4
#                            (tastystatic)    (asciiportal)
# Tkcon avec wish 8.5 : modifier /usr/share/tcltk/tkcon2.5/tkcon.tcl -> remplacer "wish" l.3 par "/usr/bin/wish8.5"
aptitude install ballz holotz-castle val-and-rick jumpnbump einstein sgt-puzzles teeworlds teeworlds-server unrar
aptitude install lua5.2 mercurial

sudo aptitude install gufw # firewall
sudo aptitude install ipython gdb grc rlwrap pandoc nmap
aptitude install moreutils build-essential aha fdupes youtube-dl poppler-utils # pdftotext
sudo aptitude install tesseract-ocr imagemagick

sudo aptitude install hddtemp && sudo pip install pysensors batinfo glances
sudo pip install requests lxml beautifulsoup scrapy coverage nose numpy scipy pandas statsmodels percol

# VLC Préferences->audio->sortie OSS pour UNIX

# Aide installation :    http://www.siteduzero.com/tutoriel-3-12827-reprenez-le-controle-avec-linux.html
#                        http://www.breizh-ardente.fr/article/avant-l-installation-les-pre-requis

# Partage Firefox (idem Thunderbird) :    http://doc.ubuntu-fr.org/tutoriel/comment_partager_ses_marques-page_entre_linux_et_windows_avec_firefox
# http://doc.ubuntu-fr.org/network-manager#eviter_les_saisies_du_mot_de_passe
# Thunderbird : smtp.orange.fr port 587 non sécurisé + suivre étapes wiki IMAG

# Désactiver GNOME Sound Login

# Importer polices Windows :
sudo mkdir /usr/share/fonts/truetype/windows
cd /usr/share/fonts/truetype/windows
sudo cp /ACER/Windows/Fonts/*.ttf .
sudo chmod +rwx *
sudo fc-cache -f -v
# Alt: aptitude install ttf-mscorefonts-installer

# /etc/fstab
# (+ option "acl" pour "/" et "/home")
# (+ retour à la ligne fin fichier ?? nécessaire)

# Réveil : connexio auto + dans Préférences/Son désactiver jingle + prog au démarrage : quodlibet --start-playing (& réglage "aléatoire")

# Pb avec icones qui se réarrangent auto : http://www.mail-archive.com/desktop-bugs@lists.ubuntu.com/msg375353.html

# RACCOURCIS :
# ALT+T : gnome-terminal --zoom=0.8 --geometry=50x29+940+50

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

# Gnome keylogger at start-up : "sudo apt-get install libpam-keyring" puis ajouter "@include common-pamkeyring" in /etc/pam.d/gdm
# Note : keyring in .gnome2/keyrings/login.keyring

# Recup ppa derrière un parefeu : edit /usr/lib/python2.6/dist-packages/softwareproperties/ppa.py -> l.88: subprocess.call(  ["apt-key", "adv", "--keyserver", "hkp://keyserver.ubuntu.com:80", ...
# FROM: http://jikan.fr/recuperer-les-clefs-gpg-des-depots-sur-ubuntu-quand-on-est-derriere-un-pare-feu/#comments

# Nvidia pilote 270 pour GeForce 525M : http://doc.ubuntu-fr.org/nvidia.run

Ubuntu Software Center : Ubuntu restricted extras, System Load Indicator # or pkg ubuntu-restricted-extras

# Clean-up unused kernels
# FROM: http://markmcb.com/2013/02/04/cleanup-unused-linux-kernels-in-ubuntu/
dpkg -l 'linux-*' | sed '/^ii/!d;/'"$(uname -r | sed "s/\(.*\)-\([^0-9]\+\)/\1/")"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d' | grep -v linux-libc-dev | xargs sudo apt-get -y purge
sudo update-grub2

# Disable overlay Scrollbars (then restart lightdm)
gsettings set org.gnome.desktop.interface ubuntu-overlay-scrollbars false # <= v12
gsettings set com.canonical.desktop.interface scrollbar-mode normal # >= v13

sudo sed -i 's/enabled=1/enabled=0/' /etc/default/apport # Disable System Crash Reports

sudo add-apt-repository ppa:nesthib/weechat-stable
sudo aptitude update && sudo aptitude install weechat python-xmpp

# http://www.techrepublic.com/blog/linux-and-open-source/pro-tip-remove-product-suggestions-from-ubuntu-unity-search-results/
System Settings > Security & Privacy > Search > Include online search results Off

# Change desktop directory
~/.config/user-dirs.dirs # edit XDG_DESKTOP_DIR

# Restore windows while keeping dual-boot:
http://askubuntu.com/questions/189410/how-do-i-reinstall-windows-7-while-keeping-my-dual-boot-configuration

ntfs-3g # IT POTENTIALLY KILL WIN7, PROCEED WITH CAUTION !

radiotray # Radios FR: http://www.xcfa.tuxfamily.org/static5/liens#RadioTray

sudo dpkg-reconfigure postfix # -> then configure local emails only => create /etc/postfix/main.cf
sudo aptitude install mailutils # provides 'mail' command

~/.config/variety/variety.conf # wallpaper changer minor change: gsettings set org.cinnamon.background picture-options centered
# Alt, ran only once: gsettings set org.gnome.desktop.background picture-options centered
# Alt: wallch

sudo apt-get install pepperflashplugin-nonfree # Flash in chromium : http://askubuntu.com/a/449266

echo 'application/x-shockwave-flash       swf swfl' > ~/.mime.types #open SWF files with Firefox

dvd+rw-mediainfo /dev/sr0 # get DVD info, alt: wodim dev=/dev/sr0 -checkdrive

Gimp -> Window -> Single Window Mode

Theme Solarized Dark pour gedit: https://github.com/mattcan/solarized-gedit


## Install from mini.iso : get network connectivity
sudo ifconfig wlan up # really needed ?
sudo killall wpa_supplicant
wpa_passphrase $SSID $WPA_KEY > wpa_passphrase.conf
sudo wpa_supplicant -iwlan0 -Dwext -fwpa_passphrase.conf
sudo dhclient -v wlan0 # dans un autre terminal
iw wlan0 link # check connexion

sudo apt-get install ubuntu-desktop

http://askubuntu.com/questions/584636/kidle-inject-causing-very-high-load
echo "blacklist intel_powerclamp" > /etc/modprobe.d/disable-powerclamp.conf


#---------
# Optimus
#---------
FROM: https://doc.ubuntu-fr.org/nvidia_optimus
"sur les portables équipés de la technologie Optimus de nombreux problèmes peuvent survenir par le simple manque de support parmi lesquels on compte notamment :
    l'impossibilité de démarrer un média d'installation (LiveCD, LiveUSB) et de manière plus générale, l'impossibilité de démarrer un Linux quelconque. Ce problème est généralement dû à un Kernel Panic provoqué par le pilote libre pour carte graphique nVidia
        problèmes de surchauffe et de ventilateur tournant à plein régime en permanence liés au fait que la carte nVidia est allumée et consomme en permanence par défaut"
-> https://doc.ubuntu-fr.org/bumblebee
Le PPA nécessite **trutset=yes**:
$ cat /etc/apt/sources.list.d/bumblebee-ubuntu-stable-xenial.list
deb [trusted=yes] http://ppa.launchpad.net/bumblebee/stable/ubuntu xenial main
# deb-src http://ppa.launchpad.net/bumblebee/stable/ubuntu xenial main

