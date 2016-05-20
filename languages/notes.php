(object) array( // Converts an array into an object
    'name' => 'name',
    'parents' => array( 'ptid' )
),

php -r "print(php_ini_loaded_file());" # find dout php.ini file used
php -r "print(phpinfo());" | grep log

error_log(print_r($variable, TRUE));

http://xdebug.org/wizard.php

new Exception()->getTraceAsString() # get a stack trace - For improved PHP exceptions formatting : jTraceEx recipe at http://php.net/manual/fr/exception.getmessage.php, that support chained exceptions and is formatted in a Java-like manner

require('/path/to/psysh');
eval(\Psy\sh()); # ensure register_argc_argv=on is set if using an old version of psysh, cf. issue #237

# PHP reference variables !!GOTCHA!!
php -r '$a = array("b" => array(0 => 42)); $x = $a["b"]; $x[0] = 7; print_r($a);'
php -r '$a = array("b" => array(0 => 42)); $x = &$a["b"]; $x[0] = 7; print_r($a);'

curl https://raw.githubusercontent.com/php/php-src/PHP-$php_version/.gdbinit >> ~/.gdbinit
gdb -p $php_script_pid
dump_bt executor_globals.current_execute_data # where is my PHP script hanging ? -> dump stacktrace

system("zip ...") >>FASTER>> standard ZipArchive lib


</-/----------\-\>
<!<! composer !>!>
<\-\----------/-/>

Ant usage :

  <target name="composer-install" description="Installing PHP dependencies" depends="get-composer">
    <exec executable="php" failonerror="true">
      <arg value="${basedir}/composer.phar" />
      <arg value="install" />
      <arg value="--prefer-source" />
      <arg value="--no-interaction" />
    </exec>
  </target>
  <target name="get-composer" description="Downloading composer" depends="check-composer" unless="${composer-phar.present}">
    <exec executable="wget" failonerror="true">
      <arg value="https://getcomposer.org/download/1.1.1/composer.phar" />
    </exec>
  </target>
  <target name="check-composer">
    <available file="composer.phar" property="composer-phar.present"/>
  </target>


</-/--------------\-\>
<!<! Drupapapapal !>!>
<\-\--------------/-/>
wget http://ftp.drupal.org/files/projects/drupal-7.38.zip && unzip drupal-7.38.zip && mv drupal-7.38 $INSTALL_DRUPAL
drush --debug ...
drush core-status && drush status-report
drush ev 'print(drush_server_home());' # find out where Drush thinks your home directory, where to put .drush/drushrc.php
drush pm-list --type=module --status=enabled # -> list modules & themes
drush site-install standard -y --account-pass=admin --db-url='mysql://root:root@localhost/my_pretty_db' --site-name=$sitename
drush en -y $modules # pm-enable - Opposite: drush dis[able]
drush ne-export --type=$content_type --file=$out_file.php
drush ne-import --uid $user_uid --file=$in_file.php
drush cc all # clear-cache
drush vget $var_name
drush watchdog-show
drush watchdog-delete all
drush updatedb
drush feature-update / feature-revert
drush eval 'var_dump(module_implements("cron"))' # List all defined cron jobs - Also, for Elysia crons: drush eval 'print_r(elysia_cron_module_jobs()); elysia_cron_initialize(); global $elysia_cron_settings_by_channel; print_r($elysia_cron_settings_by_channel)'
drush sql-query 'SELECT * FROM variable' | grep elysia_cron
drush sql-cli / $(drush sql-connect) -e "update system set schema_version=0 where name='vsct_nsr_offers';"  # Connection to DB. Second example reset the update hooks counter to 0 -> http://drupal.stackexchange.com/a/42207/52139
drush dl diff && drush en -y diff && drush features-diff $feature_name
dpm / dvm / ddebug_backtrace # devel module
drush fn-hook $hook_name # list hook implementations - Require: drush en devel -y
elasticsearch_connector/modules/elasticsearch_connector_search_api/service.inc : SearchApiElasticsearchConnector->indexItems()

chmod a+w sites/default/settings.php sites/default/files/
cat <<EOF >> sites/default/settings.php

if (file_exists(dirname(__FILE__) . '/custom_settings.php')) {
    include('custom_settings.php');
}
EOF


</-/--------------\-\>
<!<! Apapapapache !>!>
<\-\--------------/-/>
h5bp/server-configs-apache # boilerplate config
source /etc/apache2/envvars && apache2 -V # -l -L -M
sudo bash -c 'source /etc/apache2/envvars && apache2 -t && apache2ctl -S' # check config
vim /etc/apache2/sites-available/default-ssl
service apache2 restart
a2enmod / a2dismod $modname  # enable / disable std modules
ab -n5000 -c50 "http://path/to/app?params" # Apache benchmarking - Alt: tarekziade/boom
watch 'elinks -dump http://0.0.0.0/server-status | sed -n "32,70p"' # Watch Apache status (lynx cannot dump because of SSL issue)
httpd -M # list installed modules under Windows
apachectl status
ServerName localhost:80 # makes httpd startup waaay faster !
tail -F /var/log/apache2/*.log
LogLevel mod_rewrite.c:trace9 # to debug RewriteRules - in versions < 2.4 : RewriteLog ".../rewrite.log" + RewriteLogLevel 9
ForensicLog logs/forensic.log # requires: LoadModule log_forensic_module modules/mod_log_forensic.so
