#!/usr/bin/env python3
# TL;DR: pypi do not support .md READMEs, use .rst instead
# pip install readme_renderer
# https://github.com/pypa/pypi-legacy/blob/master/webui.py#L1971
import readme_renderer.rst, readme_renderer.txt, sys
with open(sys.argv[1]) as desc_file:
    desc = desc_file.read()
print(readme_renderer.rst.render(desc) or readme_renderer.txt.render(desc))
