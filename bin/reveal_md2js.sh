#!/bin/bash

# USAGE: ./reveal_md2js.sh index.md
# in HTML: <script src="$mdFilename.js" data-separator="^\n\n\n" data-separator-vertical="^\n\n" data-notes="^Note:" data-charset="utf-8"></script>

set -o pipefail -o errexit -o nounset

reveal_md2js () {
    local mdBasename="${1%.md}"
    cat <<EOF >$mdBasename.js
(function () {
'strict'
var markdownContent = ''
EOF
    sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/^/+ "/' -e 's/$/\\n"/' <$mdBasename.md >>$mdBasename.js
    cat <<EOF >>$mdBasename.js
;
var script = document.querySelector('script[src="$mdBasename.js"]');
var section = document.createElement('section');
script.parentNode.appendChild(section);
section.appendChild(document.createTextNode(markdownContent));
[].forEach.call(script.attributes, function (attr) {
    section.setAttribute(attr.name, script.getAttribute(attr.name));
});
section.setAttribute('data-markdown', '');
})();
EOF
    echo $mdBasename.js has been successfully generated
}

reveal_md2js "$@"
