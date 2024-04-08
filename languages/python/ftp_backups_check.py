#!/usr/bin/env python3
# INSTALL: pip install --user pytz
# CLI shell: lftp -u $FTP_LOGIN:$FTP_PASSWORD $FTP_HOST -e 'debug;rels;exit'  # just "debug" enables verbose mode
# Common backup-manager sources of failure:
# * network access (iptables, they differ in containers)
# * missing dependencies: Perl module Net::Lite::FTP, libz-dev...
import argparse, hashlib, os, socket, sys, tempfile
from subprocess import run
from datetime import datetime
from pytz import timezone
from ftplib import FTP, Error as FTPError


def main(args):
    if args.check_archives:
        tmp_dir = tempfile.mkdtemp()
        print(f'It is left to you to remove the temporary directory created: {tmp_dir}')

    ftp_host = os.environ['FTP_HOST']
    ftp_login = os.environ['FTP_LOGIN']
    ftp_password = os.environ['FTP_PASSWORD']
    print(f"Connecting to {ftp_login}@{ftp_host}...")
    with FTP(ftp_host) as ftp:
        # This avoids a ConnectionRefusedError during FTP.ntransfercmd() calling socket.create_connection():
        ftp.trust_server_pasv_ipv4_address = True
        if args.debug:
            ftp.set_debuglevel(2)
            sys.addaudithook(print_ftplib_audit_event)
        ftp.login(user=ftp_login, passwd=ftp_password)

        md5_per_filename = {}
        try:
            md5_lines = []
            ftp.retrlines(f'RETR chezsoi-{args.timestamp}.md5', md5_lines.append)  # on disk: /var/archives/chezsoi-hashes.md5 - not uploaded by backup-manager 0.7.12
            for md5_line in md5_lines:
                md5, filename = md5_line.split()
            md5_per_filename[filename] = md5
        except FTPError as error:
            print(error)

        files = []
        ftp.dir(files.append)
        today_files = [ls_line for ls_line in files if args.timestamp in ls_line]
        if not today_files:
            raise Exception(f'Zero files exist on FTP host matching timestamp: {args.timestamp}')
        for ls_line in today_files:
            frags = ls_line.split()
            filename, size = frags[-1], int(frags[4])
            print(f'{ls_line}  ({sizeof_fmt(size)})')  # append human readable size
            if not args.check_archives:
                continue
            file_full_path = os.path.join(tmp_dir, filename)
            print(f'Fetching {filename}...')
            with open(file_full_path, 'wb') as new_file:
                ftp.retrbinary(f'RETR {filename}', new_file.write)
            print('Checking archive integrity...')
            run(["tar", "xzf", file_full_path, "--to-stdout"], check=True)
            print(f'Successfully checked tar.gz archive {filename}')
            md5 = md5_per_filename.get(filename)
            if not md5:
                continue
            with open(file_full_path, 'rb') as fetched_file:
                computed_md5 = hashlib.md5(fetched_file.read()).hexdigest()
            if computed_md5 == md5:
                print(f'Successfully checked MD5 hash for {filename}')
            else:
                raise Exception(f'Non matching MD5 hashes: expected={md5} computed={computed_md5}')


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def print_ftplib_audit_event(event, args):
    if event.startswith("ftplib"):
        print(f'audit: {event} with args={args}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-archives', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--timestamp', default=timezone('CET').localize(datetime.utcnow()).strftime('%Y%m%d'))
    args = parser.parse_args()
    main(args)
