#!/usr/bin/env python3

# Script to extract a line with a known prefix from a PDF file.
# Used to extract the exchange rate from an AWS VAT invoice.

# Areas for improvement: extract CMap dynamically instead of using a hardcoded one

# INSTALL: pip install pdfrw

import binascii
from pdfrw import PdfReader


IN_FILEPATH = 'EUINFR21-266592.pdf'
TARGET_ANCHOR = '00010016001700010018000a00190001001a0001'.upper()  # known string prefix (encoded)
# = encode(' (1 USD = ', CMAP)


def main():
    page1_content_stream = PdfReader(IN_FILEPATH, decompress=True).pages[0].Contents.stream
    matching_line = next(line for line in page1_content_stream.split('\n') if TARGET_ANCHOR in line)
    encoded_str = matching_line.split('[')[1].split(']')[0]
    print(decode(encoded_str.lower(), CMAP))


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


# Example of /CMap extracted from a PDF /Font /ToUnicode bfchar table:
CMAP = {
    '0000': 'ffff',
    '0001': '0020',
    '0002': '002d',
    '0003': '0049',
    '0004': '006e',
    '0005': '0076',
    '0006': '006f',
    '0007': '0069',
    '0008': '0063',
    '0009': '0065',
    '000a': '0053',
    '000b': '0075',
    '000c': '006d',
    '000d': '0061',
    '000e': '0072',
    '000f': '0079',
    '0010': '0041',
    '0011': '0057',
    '0012': '0043',
    '0013': '0068',
    '0014': '0067',
    '0015': '0073',
    '0016': '0028',
    '0017': '0031',
    '0018': '0055',
    '0019': '0044',
    '001a': '003d',
    '001b': '0030',
    '001c': '002e',
    '001d': '0038',
    '001e': '0034',
    '001f': '0045',
    '0020': '0052',
    '0021': '0029',
    '0022': '0032',
    '0023': '0037',
    '0024': '002c',
    '0025': '0036',
    '0026': '0033',
    '0027': '0039',
    '0028': '006c',
    '0029': '0074',
    '002a': '0066',
    '002b': '0064',
    '002c': '0054',
    '002d': '0046',
    '002e': '0035',
    '002f': '004d',
    '0030': '007a',
    '0031': '0070',
    '0032': '0042',
    '0033': '0051',
    '0034': '006b',
    '0035': '0062',
    '0036': '0047',
    '0037': '004c',
    '0038': '0058',
    '0039': '0050',
    '003a': '0077',
    '003b': '004b',
    '003c': '0078',
    '003d': '0048',
    '003e': '004e',
    '003f': 'fb01',
    '0040': '0056',
    '0041': 'fb03',
    '0042': '004f',
}

# Other constants & functions that were useful while developping this script:

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
