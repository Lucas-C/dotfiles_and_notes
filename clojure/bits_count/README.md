BitsCount in Clojure
====================

All algorithms taken from http://graphics.stanford.edu/~seander/bithacks.html

bits_count.py
-------------

Initial version in Python. Simple copy-paste from the C algo. Do not work with -1.

bits_count.c
------------

This version was really helpful to fully understand the original C algorithm,
    notably the masks used.

To run it:

    gcc bits_count.c && ./a.out

Clojure version
---------------

'12 operations' bit count, for 32b & 64b words.

### Quickstart

Leiningen installation

    wget --no-check-certificate https://raw.github.com/technomancy/leiningen/stable/bin/lein
    sudo chmod a+x lein
    mv lein /usr/local/bin
    export LEIN_JVM_OPTS= # if using Java 1.6

Then go for it !

    lein run # '-main'
    lein test # test suite
    lein repl # Read-eval-print-loop

### Some Clojure links
- Clojure in 15min : http://adambard.com/blog/clojure-in-15-minutes/
- Clojure cheatsheet : http://clojure.org/cheatsheet
- Clojure docs : http://clojuredocs.org/clojure_core/1.3.0
- Leiningen tuto : https://github.com/technomancy/leiningen/blob/stable/doc/TUTORIAL.md
- Vim colors : https://github.com/guns/vim-clojure-static

### TODO
* implement a look-up table

