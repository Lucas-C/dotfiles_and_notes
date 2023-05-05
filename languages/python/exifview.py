#!/usr/bin/env python
# Probably only work for JPEGs
import sys
from PIL import Image, ExifTags
exif = Image.open(sys.argv[1])._getexif()
if exif:
    for k, v in sorted(exif.items()):
        print(ExifTags.TAGS.get(k, k), v)
else:
    print("Image has no EXIF metadata")
