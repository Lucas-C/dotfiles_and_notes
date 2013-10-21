#!/bin/bash
set -o pipefail -o errexit -o nounset -o xtrace

SRC_FILE=WildlifeExamLaetitia.ipynb
SRC_FILE_BASENAME=${SRC_FILE%.*}
DST_FILE=$SRC_FILE_BASENAME.html

ipython nbconvert $SRC_FILE

sed -i "s~<title>\[\]</title>~<title>$SRC_FILE_BASENAME</title>~" $DST_FILE

sed -i '
/<body>/ i\
<script type="text/javascript" src="../web-d3/local_files_and_inputs_parsing.js"></script>
' $DST_FILE
