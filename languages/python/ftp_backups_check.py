import argparse, hashlib, os, tempfile
from datetime import datetime
from pytz import timezone
from ftplib import FTP

def main(check_md5=False, debug=False):
    timestamp = timezone('CET').localize(datetime.utcnow()).strftime('%Y%m%d')
    if check_md5:
        tmp_dir = tempfile.mkdtemp()

    with FTP(os.environ['FTP_HOST']) as ftp:
        if debug:
            ftp.set_debuglevel(2)
        ftp.login(user=os.environ['FTP_LOGIN'], passwd=os.environ['FTP_PASSWORD'])

        md5_lines = []
        ftp.retrlines('RETR chezsoi-{}.md5'.format(timestamp), md5_lines.append)

        for md5_line in md5_lines:
            md5, filename = md5_line.split()
            print(filename, md5, sizeof_fmt(ftp.size(filename)))
            if not check_md5:
                continue
            file_full_path = os.path.join(tmp_dir, filename)
            with open(file_full_path, 'wb') as new_file:
                ftp.retrbinary('RETR {}'.format(filename), new_file.write)
            with open(file_full_path, 'rb') as fetched_file:
                computed_md5 = hashlib.md5(fetched_file.read()).hexdigest()
        if computed_md5 != md5:
            raise Exception('Non matching MD5 hashes: expected={} computed={}'.format(md5, computed_md5))
        print('Successfully checked MD5 hash for {}'.format(filename))

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--check-md5', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    try:
        main(args.check_md5, args.debug)
    except:
        if args.check_md5:
            print('It is left to you to remove the temporary directory created: {}'.format(tmp_dir))
