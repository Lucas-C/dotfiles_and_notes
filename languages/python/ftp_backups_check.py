#!/usr/bin/env python3
# INSTALL: pip3 install --user pytz sh
# CLI shell: lftp -u $FTP_LOGIN:$FTP_PASSWORD $FTP_HOST
import argparse, hashlib, os, sh, sys, tempfile
from datetime import datetime
from pytz import timezone
from ftplib import FTP
_ = sh(_err=sys.stderr.buffer, _out=sys.stdout.buffer)

def main(args):
    timestamp = timezone('CET').localize(datetime.utcnow()).strftime('%Y%m%d')
    if args.check_archives:
        tmp_dir = tempfile.mkdtemp()
        print('It is left to you to remove the temporary directory created: {}'.format(tmp_dir))

    with FTP(os.environ['FTP_HOST']) as ftp:
        if args.debug:
            ftp.set_debuglevel(2)
        ftp.login(user=os.environ['FTP_LOGIN'], passwd=os.environ['FTP_PASSWORD'])

        md5_lines = []
        ftp.retrlines('RETR chezsoi-{}.md5'.format(timestamp), md5_lines.append)

        for md5_line in md5_lines:
            md5, filename = md5_line.split()
            print(filename, md5, sizeof_fmt(ftp.size(filename)))
            if not args.check_archives:
                continue
            file_full_path = os.path.join(tmp_dir, filename)
            with open(file_full_path, 'wb') as new_file:
                ftp.retrbinary('RETR {}'.format(filename), new_file.write)
            with open(file_full_path, 'rb') as fetched_file:
                computed_md5 = hashlib.md5(fetched_file.read()).hexdigest()
            if computed_md5 != md5:
                raise Exception('Non matching MD5 hashes: expected={} computed={}'.format(md5, computed_md5))
            _.tar('xzf', file_full_path, '--to-stdout', _out='/dev/null')
            print('Successfully checked MD5 hash for {}'.format(filename))

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-archives', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    main(args)
