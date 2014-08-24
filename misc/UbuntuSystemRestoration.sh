apt-get install aptitude
aptitude install vim tilda git svn screen tmux g++ openjdk-7-jdk vlc chgwall
aptitude install scite nautilus-open-terminal scite grisbi texlive graphviz doxygen doxygen-gui libsdl-mixer1.2* mtpaint gaupol timidity-interfaces-extra timidity freepats most
# Fix for tilda on maverick : echo "export TERM=xterm" | sudo tee /etc/profile.d/set_term.sh && source /etc/profile
# (Système>Préférence>Clavier->Agencements->Options de l'agencement : espace insecable à tout niveau SINON pbs avec barre espace)
aptitude install tkcon libsdl1.2debian-all libaudiere-1.9.4
#							(tastystatic)	(asciiportal)
# Tkcon avec wish 8.5 : modifier /usr/share/tcltk/tkcon2.5/tkcon.tcl -> remplacer "wish" l.3 par "/usr/bin/wish8.5"
aptitude install ballz holotz-castle val-and-rick jumpnbump einstein sgt-puzzles teeworlds teeworlds-server unrar
aptitude install lua5.1 sun-java6-plugin mercurial

# VLC Préferences->audio->sortie OSS pour UNIX

# Aide installation :	http://www.siteduzero.com/tutoriel-3-12827-reprenez-le-controle-avec-linux.html
#						http://www.breizh-ardente.fr/article/avant-l-installation-les-pre-requis

# Partage Firefox (idem Thunderbird) :	http://doc.ubuntu-fr.org/tutoriel/comment_partager_ses_marques-page_entre_linux_et_windows_avec_firefox
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

# Méthode basique pour restaurer grub : booter sous livecd & sudo update-grub
https://help.ubuntu.com/community/Grub2#METHOD%203%20-%20CHROOT

# Gnome keylogger at start-up : "sudo apt-get install libpam-keyring" puis ajouter "@include common-pamkeyring" in /etc/pam.d/gdm
# Note : keyring in .gnome2/keyrings/login.keyring

# Recup ppa derrière un parefeu : edit /usr/lib/python2.6/dist-packages/softwareproperties/ppa.py -> l.88: subprocess.call(  ["apt-key", "adv", "--keyserver", "hkp://keyserver.ubuntu.com:80", ...
# FROM: http://jikan.fr/recuperer-les-clefs-gpg-des-depots-sur-ubuntu-quand-on-est-derriere-un-pare-feu/#comments

# Nvidia pilote 270 pour GeForce 525M : http://doc.ubuntu-fr.org/nvidia.run

Ubuntu Software Center : Ubuntu restricted extras, System Load Indicator # or pkg ubuntu-restricted-extras

# Clean-up unused kernels
# FROM: http://markmcb.com/2013/02/04/cleanup-unused-linux-kernels-in-ubuntu/
dpkg -l 'linux-*' | sed '/^ii/!d;/'"$(uname -r | sed "s/\(.*\)-\([^0-9]\+\)/\1/")"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d' | xargs sudo apt-get -y purge
sudo update-grub2

# Disable overlay Scrollbars (then restart lightdm)
gsettings set org.gnome.desktop.interface ubuntu-overlay-scrollbars false # <= v12
gsettings set com.canonical.desktop.interface scrollbar-mode normal # >= v13

sudo sed -i 's/enabled=1/enabled=0/' /etc/default/apport # Disable System Crash Reports

sudo aptitude install gufw # firewall
sudo aptitude install ipython gdb grc pandoc nmap

sudo add-apt-repository ppa:nesthib/weechat-stable
sudo aptitude update && sudo aptitude install weechat python-xmpp # Alt: irssi bitlbee # or mcabber for Jabber only
weechat --run-command '/set;/quit' > ~/dump-weechat-config
http://weechat.org/files/temp/scripts/hdata.py # install with '/python load hdata.py'

sudo aptitude install hddtemp && sudo pip install pysensors batinfo glances

gsettings set com.canonical.Unity.Lenses disabled-scopes "['more_suggestions-amazon.scope', 'more_suggestions-u1ms.scope', 'more_suggestions-populartracks.scope', 'music-musicstore.scope', 'more_suggestions-ebay.scope', 'more_suggestions-ubuntushop.scope', 'more_suggestions-skimlinks.scope']"

# Change desktop directory
~/.config/user-dirs.dirs # edit XDG_DESKTOP_DIR

# Restore windows while keeping dual-boot:
http://askubuntu.com/questions/189410/how-do-i-reinstall-windows-7-while-keeping-my-dual-boot-configuration

ntfs-3g
