#!/bin/sh

version=5.1.0

curl -LO https://github.com/hakimel/reveal.js/archive/$version.zip
unzip $version.zip
rm reveal.js-$version/index.html
rm reveal.js-$version/README.md
mv reveal.js-$version/* .
rm -rf CONTRIBUTING.md demo.html test/ reveal.js-$version/ $version.zip
# Fix for https://github.com/hakimel/reveal.js/issues/3659 :
cp notes.js plugin/notes/
