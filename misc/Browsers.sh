FFFFFFFFFFFFFFF
F i r e f o x
FFFFFFFFFFFFFFF
~/.mozilla/firefox/*.default/mimeTypes.rdf # FIREFOX 'open with' mapping
findImg Cache/ # all cached images - Same for Chrome
about:cache # Firefox cache infos: location, size, number of entries - chrome://cache -> to extract entries, put the 2nd hexdump section into a file and: xxd -r < dump > out.gz
about:memory # Firefox memory allocation details
about:about # all the about: pages e.g. :crashes :healthreport :permissions :plugins :sessionrestore
resource://gre-resources/
$ff_profile_dir/.parentlock # fix "Firefox is already running but is not responding" error
cp sessionstore-backups/recovery.jsonlz4 sessionstore.jsonlz4  # restore tabs from a lost session - require Firefox process to be shut down - To decode those files: https://unix.stackexchange.com/a/434882
<CTRL>+F5 # refresh page bypassing the cache
MAJ+F2: screenshot --fullpage $filename # PNG screenshot of the webpage - Alt: http://freze.it
# Useful extensions:
* uBlock
* Clippings
* ViolentMonkey
* Unhook : Remove YouTube Recommended Videos Comments
* Refined GitHub
* https://webhint.io : improve your site accessibility, speed, cross-browser compatibility
* https://github.com/tilfinltd/aws-extend-switch-roles
* https://github.com/StigNygaard/xIFr : image exif viewer
* Language Switch
* Pinterest Save Button
* Wappalyzer (resource hungry)
* Mailevelope
* OverbiteNX : gopher support, requires OverbiteNX binaries to be installed on OS
* GreaseMonkey/TamperMonkey, ChickenFoot, Scrapbook, iMacros, DejaClick # for web scrapping


https://developer.mozilla.org/en-US/docs/Tools/Web_Console
- inspect(), pprint()
- console.time(name) .timeEnd(name) .profile(name) .profileEnd(name)
- cd("#frame1"); # get into a specific iframe
- $("css selector") or $$() for ALL matches; $x("xpath expression")
//div[contains(concat(' ',normalize-space(@class),' '),' foo ')] # http://pivotallabs.com/xpath-css-class-matching/

# Enable HTTP logging - Also works un Windows by using the 'set' instead of 'export' and %TEMP% instead of /tmp
export NSPR_LOG_MODULES=timestamp,nsHttp:5,nsSocketTransport:5,nsStreamPump:5,nsHostResolver:5
export NSPR_LOG_FILE=/tmp/firefox_http.log
./firefox

$APPDATA/Mozilla/Firefox/Profiles/*/chrome/userContent.css # custom CSS - the chrome dir may not exist initially
    # -> require toolkit.legacyUserProfileCustomizations.stylesheets=true in about:config
# sqlite3 places.sqlite
    SELECT datetime(visit_date/1000000,'unixepoch') AS visit_date, url, title, visit_count
    FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id
    ORDER BY visit_date DESC LIMIT 10;


{#"#"#"#"#}
{  Chrome }
{#"#"#"#"#}
jq '.roots.bookmark_bar.children[]|select(.type=="folder" and .name=="ToCheck").children[]|{name,url}' D:\Users\lucas_cimon\AppData\Local\Google\Chrome\User Data\Default\Bookmarks
sqlite3 "$(cygpath $LOCALAPPDATA)/Google/Chrome/User Data/Default/databases/chrome-extension_loljledaigphbcpfhfmgopdkppkifgno_0/"* 'select * from fields;' # Inspect Lazarus form recovery DB
chrome://system/ -> mem_usage / tab
chrome-extension://fngmhnnpilhplaeedifhccceomclgfbg/manifest.json # Alst, in Extensions folder: for ext in ?????*; do echo $ext; jq -r .name $ext/*/manifest.json; done
CTRL + SHIFT + F : search across all files
debug(fctName) # launch debugger when fctName is called
chrome://about # list all Chrome internal pages
chrome://view-http-cache/
%LOCALAPPDATA%\Google\Chrome\User Data\Default\*Cache # 4 dirs - Alt: ~/.cache/*chrom*/Default/*Cache
python2 $code/Chromagnon/chromagnonCache.py Cache -o ~/browsable_cache
cd ~/browsable_cache
ls ???????? | wc -l
sed -n 's/.*\(Key<\/b>: http[^<]*\).*/\1\n/p' ???????? > urls
Simulate throttling: Network tab > Regular 3G
Extensions:
* Slideshow Chrome addon: https://chrome.google.com/webstore/detail/localgalleryviewerextensi/opheklanmaieaeneebdohfpbjkhcgilk -> visit /gallery.html
* Fake news debunker by InVID & WeVerify: https://chrome.google.com/webstore/detail/localgalleryviewerextensi/opheklanmaieaeneebdohfpbjkhcgilk
