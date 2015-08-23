import binascii, os, struct, sys, zlib

# Heavily inspired by Python2.7 gzip.py
# RFC: http://www.gzip.org/zlib/rfc-gzip.html#member-format

FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT = 1, 2, 4, 8, 16
KNOWN_OS = {
  0: 'FAT filesystem (MS-DOS, OS/2, NT/Win32)',
  1: 'Amiga',
  2: 'VMS (or OpenVMS)',
  3: 'Unix',
  4: 'VM/CMS',
  5: 'Atari TOS',
  6: 'HPFS filesystem (OS/2, NT)',
  7: 'Macintosh',
  8: 'Z-System',
  9: 'CP/M',
 10: 'TOPS-20',
 11: 'NTFS filesystem (NT)',
 12: 'QDOS',
 13: 'Acorn RISCOS',
255: 'unknown',
}
FIXED_HEADER_SIZE = 10
FIXED_FOOTER_SIZE = 8

def main(gzip_filename):
    gzip_file_size = os.path.getsize(gzip_filename)  # in bytes
    with open(gzip_filename, 'rb') as gzip_file:
        id1, id2 = ord(gzip_file.read(1)), ord(gzip_file.read(1))
        print('ID1+ID2: {0} {1}'.format(id1, id2))
        print('    (should be 31 139 for the file to be correctly identified as being in gzip format)')
        compression_method = ord(gzip_file.read(1))
        print('CM: {}'.format(compression_method))
        print('    (compression method: 0-7 are reserved, while 8 denotes the "deflate" method)')
        flags = ord(gzip_file.read(1))
        print('FLG: {:010b}'.format(flags))
        mtime = struct.unpack('<I', gzip_file.read(4))[0]
        print('    (last 3 bits are reserved and should always be 0)')
        if flags & FTEXT:
            print('  FTEXT flag is set: the file is probably ASCII text (optional indication)')
        if flags & FHCRC:
            print('  FHCRC flag is set: a CRC16 for the gzip header is present')
        if flags & FEXTRA:
            print('  FEXTRA flag is set: optional extra fields are present')
        if flags & FNAME:
            print('  FNAME flag is set: an original file name is present, in ISO 8859-1 (LATIN-1)')
        if flags & FCOMMENT:
            print('  FCOMMENT flag is set: a comment is present, in ISO 8859-1 (LATIN-1)')
        print('MTIME: {}'.format(mtime))
        print('    in Unix format, i.e., seconds since 00:00:00 GMT, Jan. 1, 1970')
        extra_flags = ord(gzip_file.read(1))
        print('XFL: {:010b}'.format(extra_flags))
        print('    (these flags are available for use by specific compression methods, e.g. "deflate")')
        if compression_method == 8:
            if extra_flags == 2:
                print('  deflate compression method indication: 2 => compressor used maximum compression, slowest algorithm')
            if extra_flags == 4:
                print('  deflate compression method indication: 4 => compressor used fastest algorithm')
        os_where_compressed = ord(gzip_file.read(1))
        print('OS: {}'.format(os_where_compressed))
        if os_where_compressed in KNOWN_OS:
            print('  => {}'.format(KNOWN_OS[os_where_compressed]))
        header_size = FIXED_HEADER_SIZE
        if flags & FEXTRA:
            xlen = struct.unpack('<H', gzip_file.read(2))[0]
            print('Extra field (xlen={}):'.format(xlen))
            read_extra_field(gzip_file, xlen)
            header_size += xlen
        if flags & FNAME:
            filename = read_null_terminated_string(gzip_file)
            print('Filename: {}'.format(filename))
            header_size += len(filename) + 1
        if flags & FCOMMENT:
            comment = read_null_terminated_string(gzip_file)
            print('Comment: {}'.format(comment))
            header_size += len(comment) + 1
        if flags & FHCRC:
            crc16 = struct.unpack('<H', gzip_file.read(2))[0]
            print('CRC16: {}'.format(crc16))
            header_size += 2
        compressed_data_size = gzip_file_size - header_size - FIXED_FOOTER_SIZE
        print('Compressed data length: {} bytes'.format(compressed_data_size))
        compressed_data = gzip_file.read(compressed_data_size)
        uncompressed_data = zlib.decompressobj(-zlib.MAX_WBITS).decompress(compressed_data)
        crc32 = struct.unpack('<I', gzip_file.read(4))[0]
        print('CRC32: {}'.format(crc32))
        print('  COMPUTED FROM DECOMPRESSED DATA: {}'.format(binascii.crc32(uncompressed_data) & 0xffffffff))
        isize = struct.unpack('<I', gzip_file.read(4))[0]
        print('ISIZE: {}'.format(isize))
        print('    (size of the original (uncompressed) input data modulo 2^32)')
        print('  ACTUAL DECOMPRESSED DATA SIZE: {}'.format(len(uncompressed_data)))

def read_null_terminated_string(file_stream):
    chars = []
    while True:
        char = file_stream.read(1)
        if not char or char == '\000':
            break
        chars.append(char)
    return ''.join(chars)

def read_extra_field(file_stream, length):
    """NON TESTED"""
    read_bytes_count = 0
    while read_bytes_count < length:
        si1, si2 = ord(file_stream.read(1)), ord(file_stream.read(1))
        subfield_length = struct.unpack('<H', file_stream.read(2))[0]
        print('  [Subfield] SI1+SI2: {0} {1} (length={2})'.format(si1, si2, subfield_length))
        data = file_stream.read(subfield_length)
        print('    Data: {}'.format(data))
        read_bytes_count += 4 + subfield_length

if __name__ == '__main__':
    main(sys.argv[1])
