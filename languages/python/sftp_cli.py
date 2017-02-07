#!/usr/bin/env python3

# REQUIRES: pip install pysftp

import argparse, getpass, pysftp, sys

def main(argv):
    args, remaining_argv = parse_args(argv)
    if not args.password:
        args.password = getpass.getpass(prompt='Password for user {} : '.format(args.user))
    cnopts = pysftp.CnOpts()
    if args.disable_host_key_checking:
        cnopts.hostkeys = None  # cf. http://pysftp.readthedocs.io/en/release_0.2.9/cookbook.html#pysftp-cnopts
        # also avoid a AttributeError: 'Connection' object has no attribute '_sftp_live'
    with pysftp.Connection(args.host, username=args.user, password=args.password, cnopts=cnopts) as sftp:
        with sftp.cd(args.dir):
            print(getattr(sftp, args.command)(*remaining_argv) or remaining_argv)

def parse_args(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--disable-host-key-checking', action='store_true')
    parser.add_argument('--user', required=True)
    parser.add_argument('--password')
    parser.add_argument('--host', required=True)
    parser.add_argument('--dir', required=True)
    cmd = parser.add_subparsers(dest='command')
    cmd.required = True
    cmd.add_parser('listdir')
    cmd.add_parser('get')
    cmd.add_parser('put')
    cmd.add_parser('remove')
    return parser.parse_known_args(argv)

if __name__ == '__main__':
    main(sys.argv[1:])
