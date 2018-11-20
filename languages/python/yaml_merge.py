#!/usr/bin/env python

# USAGE: ./yaml_merge.py docker-stack.yml docker-stack.preprod.yml
# REQUIRES: ruamel.yaml

# Equivalent of: yq merge --overwrite

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
        if isinstance(v, CommentedSeq):
            assert isinstance(d, CommentedSeq)
            d[k] = d.get(k, []) + v
        elif isinstance(v, CommentedMap):
            assert isinstance(d, CommentedMap)
            d[k] = dict_merge_recursive(d.get(k, CommentedMap()), v)
        elif k in d:
            raise NotImplementedError('I do not know how to merge key "{}": previous value "{}" - new value "{}"'.format(k, d[k], v))
        else:
            d[k] = v
    return d


if __name__ == '__main__':
    main(sys.argv[1:])
