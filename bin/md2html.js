#!/usr/bin/env node
'use strict';
// USAGE: md2html [--noindex] $mdFile > $htmlFile
// INSTALL: npm install -g markdown-it markdown-it-anchor markdown-it-table-of-contents markdown-it-container
var mdFilepath = process.argv[2],
    noindex = false;
if (process.argv[2] == '--noindex') {
    mdFilepath = process.argv[3];
    noindex = true;
}
require('fs').readFile(mdFilepath, 'utf8', function (err, input) {
  if (err) {
    if (err.code === 'ENOENT') {
      console.error('File not found: ' + mdFilepath);
      process.exit(2);
    }
    console.error(err.stack || err.message || String(err));
    process.exit(1);
  }
  var md = require('markdown-it')({html: true})
    .use(require('markdown-it-anchor'))
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
  process.stdout.write('<!DOCTYPE html>\n'
                     + '<html>\n'
                     + '<head>\n'
                     + '<meta charset="UTF-8">\n'
                     + '<title>' + require('path').basename(mdFilepath, '.md') + '</title>\n'
                     + (noindex ? '<meta name="robots" content="noindex">\n' : '')
                     + '</head>\n'
                     + '<body>\n');
  process.stdout.write(md.render(input));
  process.stdout.write('</body>\n'
                     + '</html>\n');
});
