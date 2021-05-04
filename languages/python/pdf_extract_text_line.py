#!/usr/bin/env python3

# Script to extract a line containing a known substring from a PDF file.
# Used to extract the exchange rate from an AWS VAT invoice.

# USAGE: ./pdf_extract_text_line.py aws-vat-invoice.pdf '1 USD = '
# INSTALL: pip install pdfrw
# ALT: https://github.com/pdfminer/pdfminer.six

import argparse, binascii
from pdfrw import PdfArray, PdfReader


def main():
    args = parse_args()
    page = PdfReader(args.pdf_filepath, decompress=True).pages[args.page_index]
    fonts = page.Resources.Font or {}
    for form in (page.Resources.XObject or {}).values():
        fonts.update(form.Resources.Font or {})
    target_substrings = [(encode(args.target_substring, font2cmap(font))[1:-1].upper(), font_id)
                                 for font_id, font in fonts.items()]
    target_substrings.append((args.target_substring, None))
    contents = page.Contents if isinstance(page.Contents, PdfArray) else [page.Contents]
    matching_line = None
    for content in contents:
        for line in content.stream.split('\n'):
            for encoded_substring, font_id in target_substrings:
                if encoded_substring in line:
                    matching_line = line
                    break  # font_id is also captured here
            if matching_line:
                break
        if matching_line:
            break
    if not matching_line:
        raise IndexError('Target substring not found in PDF on page {}'.format(args.page_index))
    matching_str = matching_line.split('[')[1].split(']')[0] if '[' in matching_line else matching_line
    if font_id is None:
        print(matching_str)
    else:
        print(decode(matching_str, font2cmap(fonts[font_id])))


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    parser.add_argument('pdf_filepath')
    parser.add_argument('target_substring')
    parser.add_argument('--page-index', type=int, default='0')
    return parser.parse_args()


def font2cmap(font):
    if font.Encoding and font.Encoding.Differences:
        raise NotImplementedError(f'font with base "{font.BaseFont}" has .Encoding.Differences')
    cmap = {}
    if not font.ToUnicode :
        return cmap
    DescendantFont = font.DescendantFonts and font.DescendantFonts[0]
    DescendantFontCIDToGIDMap = DescendantFont and DescendantFonts.CIDToGIDMap
    if DescendantFontCIDToGIDMap != '/Identity':
        raise NotImplementedError(f'font.DescendantFonts[0].CIDToGIDMap={DescendantFontCIDToGIDMap}')
    font_words = font.ToUnicode.stream.replace('\n', ' ').split(' ')
    if 'beginbfchar' in font_words:
        bfchar_table_start_index = next(i for i, word in enumerate(font_words) if word == 'beginbfchar')
        bfchar_table_end_index = next(i for i, word in enumerate(font_words) if word == 'endbfchar')
        bfchar_table_words = font_words[bfchar_table_start_index+1:bfchar_table_end_index]
        for srcCode, dstString in zip(bfchar_table_words[::2], bfchar_table_words[1::2]):
            cmap[srcCode[1:-1].lower()] = dstString[1:-1].lower()
    if 'beginbfrange' in font_words:
        bfrange_table_start_index = next(i for i, word in enumerate(font_words) if word == 'beginbfrange')
        bfrange_table_end_index = next(i for i, word in enumerate(font_words) if word == 'endbfrange')
        bfrange_table_words = font_words[bfrange_table_start_index+1:bfrange_table_end_index]
        for srcCode1, srcCode2, dstString in zip(bfrange_table_words[::3], bfrange_table_words[1::3], bfrange_table_words[2::3]):
            for srcCode in char_range(srcCode1[1:-1].lower(), srcCode2[1:-1].lower()):
                cmap[srcCode] = dstString[1:-1].lower()
    return cmap


def char_range(start, end):
    start = int.from_bytes(binascii.unhexlify(start), 'big')
    end = int.from_bytes(binascii.unhexlify(end), 'big')
    for char in range(start, end + 1):
        yield binascii.hexlify(int.to_bytes(char, 2, 'big')).decode()


def decode(s_in, cmap=None):
    s_in = s_in.lower()
    if len(s_in) > 1 and s_in[0] == '<' and s_in[-1] == '>':
        s_in = s_in[1:-1]
    assert all(c in '0123456789abcdef' for c in s_in)
    if cmap:
        s_out = ''
        assert len(s_in) % 4 == 0
        for quatuor in [s_in[4*i:4*i+4] for i in range(len(s_in) // 4)]:
            s_out += cmap[quatuor] if quatuor in cmap else quatuor
    else:
        s_out = s_in
    return binascii.unhexlify(s_out).decode()  # latin1?


def encode(s_in, cmap=None):
    s_tmp = binascii.hexlify(s_in.encode()).decode()  # latin1?
    s_tmp = ''.join(f'00{a}{b}' for a, b in zip(s_tmp[::2], s_tmp[1::2]))
    if cmap:
        inv_cmap = {v: k for k, v in cmap.items()}
        s_out = ''
        assert len(s_tmp) % 4 == 0
        for quatuor in [s_tmp[4*i:4*i+4] for i in range(len(s_tmp) // 4)]:
            s_out += inv_cmap[quatuor] if quatuor in inv_cmap else quatuor
    else:
        s_out = s_tmp
    return f'<{s_out}>'


if __name__ == '__main__':
    main()
