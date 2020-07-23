#!/bin/bash

# Install Datalogics PDF Checker on a Linux system

# USAGE: ./install-pdfchecker.sh [$install_dir_path]

set -o pipefail -o errexit -o nounset -o xtrace

DOWNLOADED_ZIP_FILENAME=PDF-CHECKER-Lin64.zip
BSX_INSTALLER_FILENAME=setup_PDF_Checker_Linux64_1.5.2.bsx
INSTALL_DIR_PATH=${1:-$PWD/PDF_Checker}

wget --no-check-certificate https://www.datalogics.com/pdflibinfo/grzqordg/che-lin64-MfeaURpvtQXzGKjY/$DOWNLOADED_ZIP_FILENAME
unzip $DOWNLOADED_ZIP_FILENAME $BSX_INSTALLER_FILENAME
rm $DOWNLOADED_ZIP_FILENAME

# Reproducing the first lines of the .bsx "Self Extracting Installer" script:
export TMPDIR=$(mktemp -d /tmp/pdfchecker.XXXXXX)
ARCHIVE=$(awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' $BSX_INSTALLER_FILENAME)
tail -q -n+$ARCHIVE $BSX_INSTALLER_FILENAME | tar xzv -C $TMPDIR
rm $BSX_INSTALLER_FILENAME

# Reproducing $TMPDIR/installer script behaviour:
mkdir -p "$INSTALL_DIR_PATH"
tar -xf $TMPDIR/PDFChecker.tar -C "$INSTALL_DIR_PATH"
rm -rf $TMPDIR
