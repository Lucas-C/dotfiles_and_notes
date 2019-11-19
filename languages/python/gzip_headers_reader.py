import gzip, os.path, struct, zlib
from sys import argv

# Heavily inspired by Python2.7 gzip.py
# RFC: http://www.gzip.org/zlib/rfc-gzip.html#member-format
# QA TODO:
#   - CLI options: --quiet --explain --optional-fields
#   - return code if check fails
#   - dissociate GzipHeader object building from printing
# +ideally, merge this into gunzip

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
GZIP_MAGIC = b'\x1f\x8b'

def main(gzip_filename):
    print('[zlib C lib version (used by Python zlib module): {}]'.format(zlib.ZLIB_VERSION))
    gzip_file_size = os.path.getsize(gzip_filename)  # in bytes
    with gzip.GzipFile(gzip_filename) as gunzipped_file_obj:
        gzip_lib_uncompressed_data = gunzipped_file_obj.read()
    print('  -> CRC32 COMPUTED FROM DATA DECOMPRESSED WITH gzip: {}'.format(zlib.crc32(gzip_lib_uncompressed_data) & 0xffffffff))
    print('  -> LENGTH OF ACTUAL DATA DECOMPRESSED with gzip : {} bytes'.format(len(gzip_lib_uncompressed_data)))
    with open(gzip_filename, 'rb') as gzip_file:
        data = gzip_file.read()
    manually_uncompress(data)

def manually_uncompress(data):
    id1, id2 = data[0], data[1]
    print('ID1+ID2: {0} {1}'.format(id1, id2))
    print('    (should be 31 139 (== \\037\\213 == GZIP_MAGIC == 1F 8B) for the file to be correctly identified as being in gzip format)')
    data = data[2:]
    compression_method = data[0]
    print('CM: {}'.format(compression_method))
    print('    (compression method: 0-7 are reserved, while 8 denotes the "deflate" method)')
    data = data[1:]
    flags = data[0]
    print('FLG: {:010b}'.format(flags))
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
    data = data[1:]
    mtime = struct.unpack('<I', data[:4])[0]
    print('MTIME: {}'.format(mtime))
    print('    in Unix format, i.e., seconds since 00:00:00 GMT, Jan. 1, 1970')
    data = data[4:]
    extra_flags = data[0]
    print('XFL: {:010b}'.format(extra_flags))
    print('    (these flags are available for use by specific compression methods, e.g. "deflate")')
    data = data[1:]
    if compression_method == 8:
        if extra_flags == 2:
            print('  deflate compression method indication: 2 => compressor used maximum compression, slowest algorithm')
        if extra_flags == 4:
            print('  deflate compression method indication: 4 => compressor used fastest algorithm')
    os_where_compressed = data[0]
    print('OS: {}'.format(os_where_compressed))
    if os_where_compressed in KNOWN_OS:
        print('  => {}'.format(KNOWN_OS[os_where_compressed]))
    data = data[1:]
    if flags & FEXTRA:
        xlen = struct.unpack('<H', data[2:])[0]
        print('Extra field (xlen={}):'.format(xlen))
        data = data[2:]
        data = read_extra_field(data, xlen)
    if flags & FNAME:
        filename, data = read_null_terminated_string(data)
        print('Filename: {}'.format(filename))
    if flags & FCOMMENT:
        comment, data = read_null_terminated_string(data)
        print('Comment: {}'.format(comment))
    if flags & FHCRC:
        crc16 = struct.unpack('<H', data[2:])[0]
        print('CRC16: {}'.format(crc16))
        data = data[2:]
    #uncompressed_data = zlib.decompress(data, -zlib.MAX_WBITS)  # => same result
    decompress_obj = zlib.decompressobj(-zlib.MAX_WBITS)
    zlib_uncompressed_data = decompress_obj.decompress(data)
    print('  -> CRC32 COMPUTED FROM DAT DECOMPRESSED WITH zlib: {}'.format(zlib.crc32(zlib_uncompressed_data) & 0xffffffff))
    print('  -> LENGTH OF ACTUAL DATA DECOMPRESSED with zlib : {} bytes'.format(len(zlib_uncompressed_data)))
    print('  -> ZLIB: len(unused_data)={}'.format(len(decompress_obj.unused_data)))
    print('  ->       eof? {}'.format(decompress_obj.eof))
    unused_data = decompress_obj.unused_data
    crc32 = struct.unpack('<I', unused_data[:4])[0]
    print('CRC32: {}'.format(crc32))
    print('    (32bits cyclic redundancy check of the original (uncompressed) input data)')
    unused_data = unused_data[4:]
    isize = struct.unpack('<I', unused_data[:4])[0]
    print('ISIZE: {} bytes'.format(isize))
    print('    (size of the original (uncompressed) input data modulo 2^32)')
    unused_data = unused_data[4:]
    if unused_data:
        print()
        print('# [Some uncompressed data remain - maybe there are extra appended files - now trying to uncompress it]')
        print()
        manually_uncompress(unused_data)

def read_null_terminated_string(data):
    chars = []
    while True:
        char, data = bytes([data[0]]), data[1:]
        if not char or char == b'\000':
            break
        chars.append(char)
    return b''.join(chars).decode('latin1'), data

def read_extra_field(data, length):
    """NON TESTED"""
    read_bytes_count = 0
    while read_bytes_count < length:
        si1, si2, subfield_length, data = data[0], data[1], struct.unpack('<H', data[2:4])[0], data[4:]
        print('  [Subfield] SI1+SI2: {0} {1} (length={2})'.format(si1, si2, subfield_length))
        subfield_data, data = data[:subfield_length], data[subfield_length:]
        print('    Data: {}'.format(subfield_data))
        read_bytes_count += 4 + subfield_length
    return data

if __name__ == '__main__':
    main(argv[1])
