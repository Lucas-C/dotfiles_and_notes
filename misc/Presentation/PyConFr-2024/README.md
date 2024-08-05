Supports de présentation pour la conférence PyConFR 2024.

## Slides setup

Requires `curl` and `unzip` :

    ./download_and_setup.sh

To launch it, you simply need to open `index.html` in your browser,
or run an HTTP server to benefit from extra *Reveal.js* features like speaker notes.

Example using Python 3 & [livereload](https://github.com/lepture/python-livereload):

    pip install livereload  # optionally: --user
    ./watch_and_serve.py
