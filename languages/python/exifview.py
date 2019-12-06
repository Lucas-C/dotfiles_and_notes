#!/usr/bin/env python
# Probably only work for JPEGs
import sys
from PIL import Image, ExifTags
for k, v in sorted(Image.open(sys.argv[1])._getexif().items()):
    print(ExifTags.TAGS.get(k, k), v)
