PHP 5 introduced explicit parameter typing: Classes, array (5.1), Interfaces, callable (5.4)

(object) array( // Converts an array into an object
    'name' => 'name',
    'parents' => array( 'ptid' )
),

php -r "print(php_ini_loaded_file());" # find dout php.ini file used
php -r "print(phpinfo());" | grep log

error_log(print_r($variable, TRUE));
fprintf(STDERR, "DEBUG: $obj\n");

http://xdebug.org/wizard.php
php --php-ini xdebug_php.ini -r 'print(xdebug_get_profiler_filename() . "\n");'
php --php-ini xdebug_php.ini .../path/to/drush.php eval "function_to_profile()"
wget --no-check-certificate https://raw.githubusercontent.com/xdebug/xdebug/master/contrib/tracefile-analyser.php
php ./tracefile-analyser.php /tmp/xdebug_trace.* memory-own 20 # cf. https://derickrethans.nl/xdebug-and-tracing-memory-usage.html & https://raw.githubusercontent.com/xdebug/xdebug/master/contrib/tracefile-analyser.php
cat xdebug_php.ini
[xdebug]
zend_extension = /tmp/xdebug-2.4.0/modules/xdebug.so
xdebug.profiler_enable = on
xdebug.profiler_output_dir = /tmp
xdebug.profiler_output_name = callgrind.out.%p.%s.%u
xdebug.profiler_append = TRUE
xdebug.auto_trace = 1
xdebug.trace_output_dir = /tmp
xdebug.trace_output_name = xdebug_trace.%p.%u
xdebug.trace_format = 1
xdebug.collect_params = 4
xdebug.collect_return = 1
xdebug.collect_vars = 1
xdebug.show_mem_delta = 1

print -r "print(new ReflectionFunction('foo'))->getFileName().PHP_EOL" # Find function source file definition
new Exception()->getTraceAsString() # get a stack trace - For improved PHP exceptions formatting : jTraceEx recipe at http://php.net/manual/fr/exception.getmessage.php, that support chained exceptions and is formatted in a Java-like manner

require(getenv('APPDATA').'\Composer\vendor\autoload.php');
eval(\Psy\sh()); # ensure register_argc_argv=on is set if using an old version of psysh, cf. issue #237

# PHP parameter passing by name !!GOTCHA!!
function foo($x = 2, $y = 3) { return $x + $y; }
foo($y = 5) // == 8 !!
# TO DETECT: ag '\([^()\n]*[^=!]=[^=>][^()\n]*\)[^{\n]*$'

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

    "require-dev": {
        "phpmd/phpmd" : "@stable",
        "mayflower/php-codebrowser": "~1.1",
        "squizlabs/php_codesniffer": "1.*",
        "phploc/phploc": "*",
        "sebastian/phpcpd": "*",
        "phpunit/phpunit": "4.3.*",
        "phpunit/phpunit-selenium": ">=1.2",
        "facebook/webdriver": "dev-master",
        "pdepend/pdepend": "2.2.*",
        "drupal/drupal-extension": "1.0.*@stable"
    },
    "config": {
        "bin-dir": ".bin/"
    }

List updates:

    composer outdated --outdated --direct

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


</-/----------------------\-\>
<!<! Standard PHP Library !>!>
<\-\----------------------/-/>
Datastructures:
- SplDoublyLinkedList
- SplStack
- SplQueue
- SplHeap
- SplMaxHeap
- SplMinHeap
- SplPriorityQueue
- SplFixedArray
- SplObjectStorage


</-/--------------\-\>
<!<! Drupapapapal !>!>
<\-\--------------/-/>
wget http://ftp.drupal.org/files/projects/drupal-7.38.zip && unzip drupal-7.38.zip && mv drupal-7.38 $INSTALL_DRUPAL
drush --debug ... # -v is at least needed to get E_WARNING msgs
drush core-status && drush status-report
drush ev 'print(drush_server_home());' # find out where Drush thinks your home directory, where to put .drush/drushrc.php
drush pm-list --type=module --status=enabled # -> list modules & themes
drush site-install standard -y --account-pass=admin --db-url='mysql://root:root@localhost/my_pretty_db' --site-name=$sitename
drush pm-enable -y $modules # opposite: drush dis[able]
drush ne-export --type=$content_type --file=$out_file.php
drush ne-import --uid $user_uid --file=$in_file.php
drush cc module-list
drush cc menu # reload hook_menu() / hook_menu_alter()
drush cc registry # reload hook_form_alter() / hook_node_save()
drush cc theme-registry / theme-list # for .tpl.php files changes - Also: drush eval 'drupal_rebuild_theme_registry(); print_r(array_keys(theme_get_registry()))'
drush cc css-js
drush vget $var_name
drush eval '$language = language_list()["fr-FR"];
drush fn-hook $hook_name # list hook implementations - Require: drush en devel -y

drush updatedb
drush feature-update / feature-revert
drush dl diff && drush en -y diff && drush features-diff $feature_name

dpm / dvm / ddebug_backtrace # devel module
drush en -y dblog && drush watchdog-show
drush watchdog-delete all

drush eval 'print_r(imagecache_presets())'
elasticsearch_connector/modules/elasticsearch_connector_search_api/service.inc : SearchApiElasticsearchConnector->indexItems()

drush sql-cli / $(drush sql-connect) -e "update system set schema_version=0 where name='vsct_nsr_offers';"  # Connection to DB. Second example reset the update hooks counter to 0 -> http://drupal.stackexchange.com/a/42207/52139
drush sql-query 'SELECT r.name, p.perm FROM role r INNER JOIN permission p ON r.rid = p.rid' | awk '{for (i=1;i<=NF;i++) $i="\""$i"\""}1' FS="\t" OFS="," > out.csv
drush sql-query 'SELECT * FROM users u WHERE u.mail="lcimon@..."' # -> get UID
drush sql-query 'SELECT r.name FROM users_roles ur LEFT JOIN role r ON r.rid=ur.rid WHERE ur.uid=...' # list a user's roles

drush eval 'var_dump(module_implements("cron"))' # List all defined cron jobs - Also, for Elysia crons: drush eval 'print_r(elysia_cron_module_jobs()); elysia_cron_initialize(); global $elysia_cron_settings_by_channel; print_r($elysia_cron_settings_by_channel)'
drush eval 'elysia_cron_initialize(); print(elysia_cron_is_channel_running("default"))' # "channels" have been renamed into "contexts" on the master branch of elysia_cron
drush eval 'elysia_cron_initialize(); elysia_cron_execute_aborted("default")' # Abort an Elysia cron channel before variable_get('elysia_cron_stuck_time', 3600) seconds
drush sql-query 'SELECT * FROM elysia_cron'
drush sql-query 'SELECT * FROM variable' | grep elysia_cron

chmod a+w sites/default/settings.php sites/default/files/
cat <<EOF >> sites/default/settings.php

if (file_exists(dirname(__FILE__) . '/custom_settings.php')) {
    include('custom_settings.php');
}
EOF

/* Deduping Drupal nodes versions to only retain the latest .vid for each one */
SELECT
    node.*
FROM content_type_blabla node
INNER JOIN
    (SELECT nid, MAX(vid) as vid
     FROM content_type_blabla
     GROUP BY nid) latest_node
ON node.nid = latest_node.nid
AND node.vid = latest_node.vid


</-/--------------\-\>
<!<! Apapapapache !>!>
<\-\--------------/-/>
h5bp/server-configs-apache # boilerplate config
source /etc/apache2/envvars && apache2 -V # -l -L -M
sudo bash -c 'source /etc/apache2/envvars && apache2 -t && apache2ctl -S' # check config
vim /etc/apache2/sites-available/default-ssl
service apache2 restart
a2enmod / a2dismod $modname  # enable / disable std modules
watch 'elinks -dump http://0.0.0.0/server-status | sed -n "32,70p"' # Watch Apache status (lynx cannot dump because of SSL issue)
httpd -M # list installed modules under Windows
apachectl status
ServerName localhost:80 # makes httpd startup waaay faster !
tail -F /var/log/apache2/*.log
LogLevel mod_rewrite.c:trace9 # to debug RewriteRules - in versions < 2.4 : RewriteLog ".../rewrite.log" + RewriteLogLevel 9
ForensicLog logs/forensic.log # requires: LoadModule log_forensic_module modules/mod_log_forensic.so
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" **%T/%D**" combined  # server response time


<[-----]>
<[Nginx]>
<[-----]>
nginx -t  # help diagnosing service start failure
yandex/gixy  # configuration static analyzer in Python to prevent security misconfiguration and automate flaw detection
https://news.ycombinator.com/item?id=14617879 # speed-up advices
