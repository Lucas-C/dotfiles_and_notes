'use strict';
// CLI USAGE: md2html [--noindex] [--mincss] $mdFile > $htmlFile
// INSTALL: npm install -g markdown-it markdown-it-anchor git+https://git@github.com/Lucas-C/markdown-it-checkbox.git markdown-it-header-sections markdown-it-table-of-contents markdown-it-container markdown-it-include markdown-it-multimd-table markdown-it-smartarrows minimist
const ANCHOR_ID_CHAR_RANGE_TO_IGNORE = '[\x00-\x2F\x3A-\x40\x5B-\x60\x7B-\uFFFF]+';

function slugify(s) {
  s = String(s)
  s = s.trim()
  s = s.toLowerCase()
  s = s.replace(new RegExp('^'+ANCHOR_ID_CHAR_RANGE_TO_IGNORE, 'g'), '')
  s = s.replace(new RegExp(ANCHOR_ID_CHAR_RANGE_TO_IGNORE, 'g'), '-')
  return encodeURIComponent(s);
}

function md2html(input) {
  var md = require('markdown-it')({html: true, linkify: true, typographer: true})
    .use(require('markdown-it-anchor'), { slugify: slugify } )
    .use(require('markdown-it-checkbox'))
    .use(require('markdown-it-header-sections'))
    .use(require('markdown-it-include'))
    .use(require('markdown-it-multimd-table'), {enableMultilineRows: true})
    .use(require('markdown-it-smartarrows'))
    .use(require('markdown-it-table-of-contents'))
    .use(require('markdown-it-container'), 'classname', {
      validate: name => name.trim().length, // allow everything not empty
      render: (tokens, idx) => {
        if (tokens[idx].nesting === 1) {
          return `<div class="${tokens[idx].info.trim()}">\n`;
        }
        return '</div>\n';
      }
    });
    return md.render(input);
}

if (require.main === module) { // means we are executed as a script
  var args = require('minimist')(process.argv.slice(2), {boolean: true}),
      mdFilepath = args._[0];
  require('fs').readFile(mdFilepath, 'utf8', function (err, input) {
    if (err) {
      if (err.code === 'ENOENT') {
        console.error('File not found: ' + mdFilepath);
        process.exit(2);
      }
      console.error(err.stack || err.message || String(err));
      process.exit(1);
    }
    process.stdout.write('<!DOCTYPE html>\n'
                        + '<html>\n'
                        + '<head>\n'
                        + '<meta charset="UTF-8">\n'
                        + '<title>' + require('path').basename(mdFilepath, '.md') + '</title>\n'
                        + (args.noindex ? '<meta name="robots" content="noindex">\n' : '')
                        + '</head>\n'
                        + '<body>\n');
    if (args.mincss) {
      process.stdout.write('<style type="text/css">\n'
                          + 'body { margin: 40px auto; max-width: 650px; line-height: 1.6; font-family: sans-serif; color: #444; padding:0 10px; text-align:justify; }\n'
                          + 'h1, h2, h3 { line-height: 1.2; }\n'
                          + 'blockquote { font-style: italic; border-left: 2px solid #eee; padding-left: 18px; }\n'
                          + 'img { display: block; margin: 0 auto; max-width: 100%; }\n'
                          + 'figcaption { font-size: x-small; text-align: center; }\n'
                          + 'table { border-spacing: 0; border-collapse: collapse; page-break-inside: avoid; } td { padding: 5px; border-top: 1px solid #ddd; } tbody > tr:nth-of-type(odd) { background-color: #f9f9f9; }\n'
                          + '@media (min-width: 1278px) { .toc { position: fixed; left: 0; width: 25%; font-size: small; } }\n'
                          + '</style>\n');
    }
    process.stdout.write(md2html(input));
    process.stdout.write('</body>\n'
                     + '</html>\n');
  });
}

// To convert Markdown to HTML "on the fly" in your browser using this code, you will need to:
// 1. Tell your server to return a text/html Content-Type for your .md files
// 2. Bundle this file using: browserify md2html.js > md2html.bundle.js
// 3. Place this at the bottom or top of your .md file: <script src="md2html.bundle.js"></script>
if (typeof window !== 'undefined') { // means we are executed in a browser
  window.onload = () => {
    const div = document.createElement('div');
    // We move any existing <style> tag to the document <head> to ignore them:
    for (const styleElem of document.body.getElementsByTagName('style')) {
      document.head.appendChild(styleElem);
    }
    for (const linkElem of document.body.getElementsByTagName('link')) {
      document.head.appendChild(linkElem);
    }
    div.innerHTML = md2html(document.body.innerHTML);
    document.body.innerHTML = '';
    document.body.append(div.children[0]);
  };
}
