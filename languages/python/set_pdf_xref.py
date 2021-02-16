#!/usr/bin/env python3

# Script to re-build a PDF xref table after manually editing a PDF.

# USAGE: ./set_pdf_xref.py in.pdf [--inplace|out.pdf]

import re, sys


def main():
    input_filepath = sys.argv[1]
    if len(sys.argv) > 2:
        output_filepath = input_filepath if sys.argv[2] == '--inplace' else sys.argv[2]
    else:
        output_filepath = 'out-' + input_filepath
        print('Generating output to:', output_filepath)

    with open(input_filepath, 'rb') as input_file:
        data = input_file.read()

    # Build xref table:
    xref_start = data.index(b'\nxref\n') + len('\nxref\n')
    xref_end = data.index(b'trailer ', xref_start)
    xref_table, obj_index = ['0000000000 65535 f '], None
    for match in re.findall(b'[0-9]+ 0 obj\n', data):
        obj_index = data.index(match, obj_index)
        xref_table.append(f'{obj_index:010} 00000 n ')
    xref_table.insert(0, f'0 {len(xref_table)}')
    data = data[:xref_start] + '\n'.join(xref_table).encode() + data[xref_end:]

    # Update startxref:
    xref_pos = data.index(b'\nxref') + 1
    startxref_start = data.index(b'\nstartxref\n') + len('\nstartxref\n')
    startxref_end = data.index(b'\n', startxref_start)
    if xref_pos != int(data[startxref_start:startxref_end]):
        data = data[:startxref_start] + str(xref_pos).encode() + data[startxref_end:]

    with open(output_filepath, 'wb') as output_file:
        output_file.write(data)

    # from pdfrw import PdfReader, PdfWriter
    # out = PdfWriter()
    # out.addpage(PdfReader(fdata=data).pages[0])
    # out.write(output_filepath)


if __name__ == '__main__':
    main()
