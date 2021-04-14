#!/usr/bin/env python3

# Script to extract a line containing a known substring from a PDF file.
# Used to extract the exchange rate from an AWS VAT invoice.

# USAGE: ./pdf_extract_text_line.py EUINFR21-266592.pdf '1 USD = '
# INSTALL: pip install pdfrw

import argparse, binascii
from pdfrw import PdfReader


def main():
    args = parse_args()
    page = PdfReader(args.pdf_filepath, decompress=True).pages[args.page_index]
    encoded_target_substrings = [(encode(args.target_substring, font2cmap(font))[1:-1].upper(), font_id)
                                 for font_id, font in page.Resources.Font.items()]
    matching_line = None
    for i, line in enumerate(page.Contents.stream.split('\n')):
        for encoded_substring, font_id in encoded_target_substrings:
            if encoded_substring in line:
                matching_line = line
                break  # font_id is also captured here
        if matching_line:
            break
    else:
        raise IndexError('Target substring not found in PDF on page {}'.format(args.page_index))
    encoded_str = matching_line.split('[')[1].split(']')[0]
    font = page.Resources.Font[font_id]
    print(decode(encoded_str.lower(), font2cmap(font)))


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('pdf_filepath')
    parser.add_argument('target_substring')
    parser.add_argument('--page-index', type=int, default='0')
    return parser.parse_args()


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
