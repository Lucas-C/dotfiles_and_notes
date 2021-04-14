#!/usr/bin/env python3

# Script to extract a line with a known prefix from a PDF file.
# Used to extract the exchange rate from an AWS VAT invoice.

# INSTALL: pip install pdfrw

import binascii
from pdfrw import PdfReader


IN_FILEPATH = 'EUINFR21-266592.pdf'
TARGET_ANCHOR = '00010016001700010018000a00190001001a0001'.upper()  # known string prefix (encoded)
# = encode(' (1 USD = ', CMAP)


def main():
    page = PdfReader(IN_FILEPATH, decompress=True).pages[0]
    lines = page.Contents.stream.split('\n')
    for i, line in enumerate(lines):
        if TARGET_ANCHOR in line:
            matching_line = line
            break
    assert matching_line
    for j in range(i - 1, 0, -1):
        line = lines[j]
        if ' /F' in line:
            font_id = next(word for word in line.split(' ') if word.startswith('/F'))
            break
    assert font_id  # would allow to retrieve the CMap def in the /Page > /Resources > /Font dict
    font = page.Resources.Font[font_id]
    encoded_str = matching_line.split('[')[1].split(']')[0]
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


def decode_multilines(page_content_stream, cmap):
    "Decode all strings in a page object stream from a PDF file formatted with qpdf --qdf"
    s = ''
    for line in page_content_stream.split('\n'):
        if line.startswith('<'):
            s += line.split(' ', 1)[0][1:-1]
    return decode(s, cmap)


if __name__ == '__main__':
    main()
