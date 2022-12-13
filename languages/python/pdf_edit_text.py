#!/usr/bin/env python3
# Example of modifying some characters in a PDF
import sys
from binascii import hexlify, unhexlify
from pdfrw import PdfReader, PdfWriter
from pdfrw.compress import compress
from pdfrw.uncompress import uncompress

from pdf_extract_text_line import font2cmap

reader = PdfReader(sys.argv[1])
page = reader.pages[0]
is_compressed = page.Contents.Filter
if is_compressed:
    assert uncompress([page.Contents])

def decode(s_in, cmap):
    s_out = ""
    for c in s_in:
        c = ord(c)
        if not c: continue
        c = hexlify(int.to_bytes(c, 2, 'big')).decode()
        c = cmap[c]
        c = int.from_bytes(unhexlify(c), 'big')
        s_out += chr(c)
    return s_out

target_font = "/F"  # déterminée à partir de la dernière instruction Tf dans le stream avant la ligne cible
cmap = None
for form in (page.Resources.XObject or {}).values():
    if form.Resources and form.Resources.Font:
        for font_id, font in form.Resources.Font.items():
            if font_id == target_font:
                cmap = font2cmap(font)

line_i = 46  # la ligne d'instructions qui nous intéresse
             # NOTE: fonctionne uniquement parce que le stream est découpé avec une instruction par ligne
line = page.Contents.stream.splitlines()[line_i]
print(line)
print("stream:", "|".join(str(ord(c)) for c in line))
print(decode(line[1:-3], cmap))

# Le mapping de caractères a initialement été déduit empiriquement :
print(f"    chr(128) = chr(0x80) => l")
print(f"    chr(129) = chr(0x81) => t")
print("...")
print(f"¢ = chr(162) = chr(0xa2) => D")
print(f"¤ = chr(163) = chr(0xa3) => c")
print("...")
print(f"¨ = chr(168) = chr(0xa8) => 2")
print("...")
print(f"Ð = chr(208) = chr(0xd0) => 3")
print(f"Ñ = chr(209) = chr(0xd1) => /")
print(f"Ò = chr(210) = chr(0xd2) => 1")
print("...")
print(f"â = chr(226) = chr(0xe2) => bold 3")

# On construit un encoder :
inv_cmap = {}
for k, v in cmap.items():
    if v not in inv_cmap or k < "00e0":  # arbitrary value to select the correct characters,
                                         # when there are several mappings to the same dest unicode char
        inv_cmap[v] = k
assert decode("1", inv_cmap) == "Ò"
assert decode("2", inv_cmap) == "¨"
assert decode("3", inv_cmap) == "Ð"

print("6 is encoded as:", decode("6", inv_cmap))

# La modification effective :
def stream_set(page, i, new_char):
    page.Contents.stream = page.Contents.stream[:i] + new_char + page.Contents.stream[i+1:]
# Les indices ont été déterminés en identifiant la structure de la string passée à Tf,
# qui est formée de "2-bytes characters" séparés par des \0
stream_set(page, i=1010, new_char="Ò")  # 2 -> 1
stream_set(page, i=1026, new_char="¨")  # 1 -> 2
stream_set(page, i=1028, new_char="¨")  # 5 -> 2

# stream_set(page, i=1012, new_char="E")  # 3 -> 6
# NOTE : impossible d'insérer un 6, car le seul 6 présent dans le document était dans le footer,
#        avec un style visuel non différent.
#        Le caractère "6" standard n'était pas inclus dans le "font subset" du PDF source.

line = page.Contents.stream.splitlines()[line_i]
print(line)
print("stream:", "|".join(str(ord(c)) for c in line))
print(decode(line[1:-3], cmap))

if is_compressed:
    compress([page.Contents])

writer = PdfWriter()
writer.pagearray = reader.Root.Pages.Kids
writer.write("out.pdf")
