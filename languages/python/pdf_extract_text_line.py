#!/usr/bin/env python3

# Script to extract a line containing a known substring from a PDF file.
# Used to extract the exchange rate from an AWS VAT invoice.

# INSTALL: pip install pdfrw

import binascii
from pdfrw import PdfReader


IN_FILEPATH = 'EUINFR21-266592.pdf'
TARGET_SUBSTRING_ENCODED = '001700010018000a00190001001a0001'.upper()  # = encode('1 USD = ', CMAP)


def main():
    page = PdfReader(IN_FILEPATH, decompress=True).pages[0]
    lines = page.Contents.stream.split('\n')
    for i, line in enumerate(lines):
        if TARGET_SUBSTRING_ENCODED in line:
            matching_line = line
            break
    assert matching_line
    encoded_str = matching_line.split('[')[1].split(']')[0]
    # Retrieve the latest font selected with Tf before that line:
    for j in range(i - 1, 0, -1):
        line = lines[j]
        if ' /F' in line:
            font_id = next(word for word in line.split(' ') if word.startswith('/F'))
            break
    assert font_id
    font = page.Resources.Font[font_id]
    print(decode(encoded_str.lower(), font2cmap(font)))


def font2cmap(font):
    if not font.ToUnicode:
        return None
    font_lines = font.ToUnicode.stream.split('\n')
    bfchar_table_start_index = next(i for i, line in enumerate(font_lines) if line.endswith('beginbfchar'))
    bfchar_table_end_index = next(i for i, line in enumerate(font_lines) if line.endswith('endbfchar'))
    bfchar_table_lines = font_lines[bfchar_table_start_index+1:bfchar_table_end_index]
    cmap = {}
    for line in bfchar_table_lines:
        a, b = line.split(' ')
        cmap[a[1:-1]] = b[1:-1]
    return cmap


def decode(s_in, cmap=None):
    if len(s_in) > 1 and s_in[0] == '<' and s_in[-1] == '>':
        s_in = s_in[1:-1]
    if cmap:
        s_out = ''
        for quatuor in [s_in[4*i:4*i+4] for i in range(len(s_in) - 3)]:
            s_out += cmap[quatuor] if quatuor in cmap else quatuor
    else:
        s_out = s_in
    return binascii.unhexlify(s_out).decode()


def encode(s_in, cmap=None):
    s_tmp = binascii.hexlify(s_in.encode()).decode()
    s_tmp = ''.join(f'00{a}{b}' for a, b in zip(s_tmp[::2], s_tmp[1::2]))
    if cmap:
        inv_cmap = {v: k for k, v in cmap.items()}
        s_out = ''
        for quatuor in [s_tmp[4*i:4*i+4] for i in range(len(s_tmp) - 3)]:
            s_out += inv_cmap[quatuor] if quatuor in inv_cmap else quatuor
    else:
        s_out = s_tmp
    return f'<{s_out}>'


if __name__ == '__main__':
    main()
