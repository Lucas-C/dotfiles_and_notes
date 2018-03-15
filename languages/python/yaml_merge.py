#!/usr/bin/env python

# USAGE: ./yaml_merge.py docker-stack.yml docker-stack.preprod.yml
# REQUIRES: ruamel.yaml

# Equivalent of: yq merge --overwrite
# **but lists are REPLACED, not merged**

import sys
import ruamel.yaml as yaml
from ruamel.yaml.comments import CommentedMap


def main(file_paths):
    with open(file_paths[0]) as yaml_file:
        result = yaml.load(yaml_file, Loader=yaml.RoundTripLoader)
    for file_path in file_paths[1:]:
        with open(file_path) as yaml_file:
            dict_update(result, yaml.load(yaml_file, Loader=yaml.RoundTripLoader))
    yaml.dump(result, sys.stdout, Dumper=yaml.RoundTripDumper)

def dict_update(d, u):
    for k, v in u.items():
        d[k] = dict_update(d.get(k, CommentedMap()), v) if isinstance(v, CommentedMap) else v
    return d


if __name__ == '__main__':
    main(sys.argv[1:])
