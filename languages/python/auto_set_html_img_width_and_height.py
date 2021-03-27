#!/usr/bin/env python3
import argparse, sys

# Insert height & width attributes on all <img> tags based on the source image actual dimensions.

# WHY? cf. https://web.dev/optimize-cls/
# > Always include width and height size attributes on your images and video elements, to ensure that the browser can allocate the correct amount of space in the document while the image is loading.

# INSTALL: pip install Pillow

# Implementation details:
# * we dot not rely on external libs like BeautifulSoup, because none provides indentation-preserving formatting:
#   we favor NOT altering HTML formatting, even if that means not supporting <img> tags spanning multiple lines.

# Note: this could easily be made into a pre-commit hook

import re
from PIL import Image


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('html_filepaths', nargs='*', help='Paths to HTML files to edit')
    args = parser.parse_args(argv)
    for html_filepath in args.html_filepaths:
        with open(html_filepath) as html_file:
            html = html_file.read()
        with open(html_filepath, 'w') as html_file:
            html_file.write(re.sub('<img[^>]+>', repl_img, html))

def repl_img(match):
    img_tag = match.group()
    src_match = re.search(' src=["\']([^"\']+)', img_tag)
    assert src_match, f'Found <img> tag with no "src" attribute: {img_tag}'
    src_img_filepath = src_match.group(1)
    if src_img_filepath.endswith('.svg'):
        return img_tag
    img_tag = re.sub(' width=["\'][^"\']+["\']', '', img_tag)
    img_tag = re.sub(' height=["\'][^"\']+["\']', '', img_tag)
    width, height = Image.open(src_img_filepath).size
    return f'<img width="{width}" height="{height}" {img_tag[5:]}'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
