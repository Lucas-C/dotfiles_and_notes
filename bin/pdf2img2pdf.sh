#!/bin/bash
# USAGE: ./pdf2img2pdf.sh file.pdf [--landscape]
set -o pipefail -o errexit -o nounset

# $DENSITY can be defined before calling this script
[ -n "${DENSITY:-}" ] || DENSITY=600

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
SRC_PDF="$1"; shift

TMP_DIR=$(mktemp -d)
cp -t "$TMP_DIR" "$SRC_PDF"
cd "$TMP_DIR"
SRC_PDF_NAME=$(basename "$SRC_PDF")

# Calling ImageMagick:
convert -density "$DENSITY" "$SRC_PDF_NAME" tmp-%03d.png
rm "$SRC_PDF_NAME"
$SCRIPT_DIR/a4-from-imgs.py "$@" --no-margin tmp-*.png
DST_FILE="$OLDPWD/fromImgs-d$DENSITY-$SRC_PDF_NAME"
mv *.pdf "$DST_FILE"
echo "Moved to $DST_FILE"

cd "$OLDPWD"
rm -rf "$TMP_DIR"
