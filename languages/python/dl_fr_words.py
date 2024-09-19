#!/usr/bin/env python3
import requests
try:  # optional dependency
    from tqdm import tqdm
except ImportError:
    tqdm = lambda _: _

START_TAG = "<span class=mt>"
END_TAG = "</span>"

UPPERCASE_WORDS = []
suffixes = [""] + [f"page{i}" for i in range(2, 1549)]
for suffix in tqdm(suffixes):
    resp = requests.get(f"https://www.listesdemots.net/touslesmots{suffix}.htm")
    resp.raise_for_status()
    html = resp.text
    start_tag_i = html.index(START_TAG)
    start_i = start_tag_i + len(START_TAG)
    end_tag_i = html.index(END_TAG, start_i)
    UPPERCASE_WORDS += html[start_i:end_tag_i].split(" ")
print(f"{len(UPPERCASE_WORDS)} words extracted, now writing to file...")
with open("listesdemots.net.txt", "w", encoding="utf-8") as out_file:
    out_file.write("\n".join(UPPERCASE_WORDS))
