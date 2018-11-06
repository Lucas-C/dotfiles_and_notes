#!/usr/bin/env python
import sys
import piexif
from PIL import ExifTags, Image

img_path, text_key, value = sys.argv[1:]
img = Image.open(img_path)
exif_info = piexif.load(img.info['exif'])

exif_category, numeric_key = next((ec, nk) for ec, d in exif_info.items() if ec != 'thumbnail'
                                           for nk in d.keys() if ExifTags.TAGS[nk] == text_key)
exif_info[exif_category][numeric_key] = int(value)

exif_bytes = piexif.dump(exif_info)
img.save(img_path, exif=exif_bytes)
