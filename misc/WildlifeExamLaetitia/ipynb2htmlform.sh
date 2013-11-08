#!/bin/bash
set -o pipefail -o errexit -o nounset -o xtrace

SRC_FILE=${1?'Missing .ipynb IPython notebook file as parameter'}
SRC_FILE_BASENAME=${SRC_FILE%.*}
DST_FILE=$SRC_FILE_BASENAME.html

ipython nbconvert $SRC_FILE

sed -i "s~<title>\[\]</title>~<title>$SRC_FILE_BASENAME</title>~" $DST_FILE

sed '/<body>/,$d' $DST_FILE > $DST_FILE.tmp
echo '<script type="text/javascript">' >> $DST_FILE.tmp
cat ../web-d3/local_files_and_inputs_parsing.js >> $DST_FILE.tmp
echo '</script>' >> $DST_FILE.tmp
sed -n '/<body>/,$p' $DST_FILE >> $DST_FILE.tmp
mv $DST_FILE.tmp $DST_FILE

