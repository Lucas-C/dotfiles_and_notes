#!/usr/bin/env python3

# Script to retrieve download counts from nginx logs configured this way:
#
#    log_format download '$time_local $status $http_x_forwarded_for "$uri" $http_user_agent';
#    location ~^regex-pattern$  {
#        access_log /var/log/nginx/log-name.log download;
#    }

# USAGE: ./nginx_logs_stats.py $pattern_name

import gzip, re, sys
from collections import defaultdict
from glob import glob


def main(log_name):
    monthly_stats_per_filename = defaultdict(lambda: defaultdict(int))

    for file_path in glob(f'/var/log/nginx/{log_name}*'):
        if file_path.endswith('.gz'):
            with gzip.open(file_path) as log_file:
                log_lines = [line.decode().strip() for line in log_file.readlines()]
        else:
            with open(file_path) as log_file:
                log_lines = [line.strip() for line in log_file.readlines()]
        for log_line in log_lines:
            month = log_line[3:6]
            if '"' in log_line:
                quote1_index = log_line.index('"')
                quote2_index = log_line.index('"', quote1_index + 1)
                filename = log_line[quote1_index+1:quote2_index]
            else:  # Backward compatibility when $uri was not enclosed in quotes in log_format:
                space_index = -1
                for _ in range(4):
                    space_index = log_line.index(' ', space_index+1)
                pdf_ext_index = log_line.index('.pdf')
                filename = log_line[space_index+1:pdf_ext_index+4]
            monthly_stats_per_filename[filename][month] += 1

    for filename, stats in sorted(monthly_stats_per_filename.items()):
        print(f'# {filename} download counts:')
        for month, count in stats.items():
            print(f'  {month}: {count}')
        print()


if __name__ == '__main__':
    main(sys.argv[1])

