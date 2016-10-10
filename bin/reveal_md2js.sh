#!/bin/bash

# cf. https://github.com/hakimel/reveal.js/issues/673

# USAGE: ./reveal_md2js.sh .css_selector [separator=...] [verticalSeparator=...] [notesSeparator=...] [attributes=...] < slides.md > slides.js

# in HTML:
#   <section class="css_selector"></section>
#   <script src="slides.js"></script>

set -o pipefail -o errexit -o nounset -o xtrace

main () {
    local css_selector="$1"
    shift
    local separator='^\n\n\n'
    local verticalSeparator='^\n\n'
    local notesSeparator='^Note:'
    local attributes='charset="utf-8"'
    cat <<EOF
document.addEventListener('ready', function () {
'strict'
var section = document.querySelector('$css_selector');
var markdownContent = ''
EOF
    sed -e 's/\\/\\\\/' -e 's/"/\\"/' -e 's/^/+ "/' -e 's/$/\\n"/'
    cat <<EOF
;
section.outerHTML = RevealMarkdown.slidify( markdownContent, {
    separator: '$separator',
    verticalSeparator: '$verticalSeparator',
    notesSeparator: '$notesSeparator',
    attributes: '$attributes'
});
RevealMarkdown.convertSlides();
Reveal.triggerKey(36/*HOME*/);
});
EOF
}

main "$@"
