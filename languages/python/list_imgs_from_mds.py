#!/usr/bin/env python3
import html5lib, sys
from CommonMark import commonmark  # Alt: https://github.com/Lucas-C/pelican-mg/blob/master/gen_imgs_from_mds.py

for md_file_path in sys.argv[1:]:
    with open(md_file_path) as md_file:
        md_content = md_file.read()
    html = commonmark(md_content)
    doc_root = html5lib.parse(html)
    for img in doc_root.iter('{http://www.w3.org/1999/xhtml}img'):
        print(img.attrib['src'])
