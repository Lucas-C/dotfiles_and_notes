### Installation & upstart script

https://help.ubuntu.com/community/Etherpad-liteInstallation
https://chezsoi.org/lucas/blog/2014/10/10/en-setting-up-etherpad-in-a-server-subdirectory-aka-apache-config-hell/

### Server setup

https://github.com/ether/etherpad-lite/wiki/How-to-put-Etherpad-Lite-behind-a-reverse-Proxy
http://stackoverflow.com/a/13385407

    sudo apt-get install libapache2-mod-proxy-html libxml2-dev
    sudo a2enmod proxy_html xml2enc

### DB setup

https://github.com/ether/etherpad-lite/wiki/How-to-use-Etherpad-Lite-with-MySQL

    mysqladmin --defaults-file=/etc/mysql/debian.cnf create etherpad-db
    read -s pswd
    mysql --defaults-file=/etc/mysql/debian.cnf -e "grant all privileges on `etherpad-db`.* to 'etherpad'@'localhost' identified by '$pswd';"
    # ... bin/run.sh
    mysql --defaults-file=/etc/mysql/debian.cnf "\
        alter database `etherpad-db` character set utf8 collate utf8_bin;\
        use `etherpad-db`;\
        alter table `store` convert to character set utf8 collate utf8_bin;"

### Plugins management

    npm install ep_previewimages ep_small_list ep_historicalsearch ep_timesliderdiff ep_author_hover
    sudo -u etherpad nohup bin/run.sh &

    sed -i 's~"/static/~"static/~' node_modules/ep_small_list/index.js
    grep -IRFl '"/static/' node_modules/ep_syntaxhighlighting/ | xargs sed -i 's~"/static/~"../static/~'

### Pads listing / deletion

https://github.com/ether/etherpad-lite/wiki/How-to-list-all-pads

    sudo mysql --defaults-file=/etc/mysql/debian.cnf etherpad-db -e 'select store.key from store' \
       | grep -Eo '^pad:[^:]+' \
       | sed -e 's/pad://' \
       | sort \
       | uniq -c \
       | sort -rn # first number == change counts, 2 => empty pad

    curl "http://$pad_url/api/1/deletePad?apikey=$api_key&padID=$pad_id"
