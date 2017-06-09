#!/bin/bash

set -o pipefail -o errexit -o nounset -o xtrace

cd $(dirname ${BASH_SOURCE})

version=3.5.0

wget https://github.com/hakimel/reveal.js/archive/$version.zip
unzip $version.zip
rm reveal.js-$version/index.html
mv reveal.js-$version/* .
rm -rf CONTRIBUTING.md  demo.html test/ reveal.js-$version/ $version.zip
cat <<EOF >>css/theme/solarized.css
.reveal:before {
    content: 'Lucas Cimon @ VSCT';
    font-size: large;
    position: fixed;
    top: 5%;
    right: 5%;
}

.reveal {
    background-image: url(../../VSCT_logo.png);
    background-size: 15%;
    background-repeat: no-repeat;
    background-position: 95% 10%;
}
EOF

wget https://chezsoi.org/lucas/slides/python_frameworks_web_2016-02-26/VSCT_logo.png
wget https://www.lua.org/images/lua-logo.gif
