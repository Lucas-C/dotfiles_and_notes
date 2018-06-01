#!/usr/bin/env node
'use strict';
// USAGE: md2html [--noindex] [--mincss] $mdFile > $htmlFile
// INSTALL: npm install -g markdown-it markdown-it-anchor markdown-it-table-of-contents markdown-it-container markdown-it-include markdown-it-multimd-table minimist
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
  var md = require('markdown-it')({html: true, linkify: true, typographer: true})
    .use(require('markdown-it-anchor'))
    .use(require('markdown-it-include'))
    .use(require('markdown-it-multimd-table'), {enableMultilineRows: true})
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
  process.stdout.write(md.render(input));
  process.stdout.write('</body>\n'
                     + '</html>\n');
});
