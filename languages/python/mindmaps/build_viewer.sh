#!/bin/bash

set -o pipefail -o errexit -o nounset -o xtrace

[ -d wisemapping-open-source ] || git clone https://bitbucket.org/wisemapping/wisemapping-open-source.git
rsync --verbose --recursive --files-from=rsync.include --copy-links wisemapping-open-source .

# Allowing for query params
sed -i "s/mapId = 'welcome'/mapId = location.search.substr(1) || 'welcome'/" wise-editor/src/main/webapp/html/viewmode.html

# Fixing ugly pom.xml-based JS loading
cd mindplot/src/main/javascript
cat $(sed -n '/<includes>/,/<\/includes>/{/<includes>/d;/<\/includes>/d;p}' ../../../../wisemapping-open-source/mindplot/pom.xml | sed -e 's~${basedir}~../../..~' -e 's~\s*<include>~~' -e 's~</include>$~~') > ../../../../wise-editor/src/main/webapp/js/mindplot-bundle.js
cd -
sed -i '$s~.*~$.ajax({url: "js/mindplot-bundle.js", dataType: "script", cache: true});~' wise-editor/src/main/webapp/js/editor.js

