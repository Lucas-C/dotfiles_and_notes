% VIM_CHEAT_SHEET

Files
=====
- vim __can open__ .gz files
- *:w* __new_filename__ : save a copy and keep working on original
- *vim -r* __file.swp__ : restore a file after a crash
- *vim -p* __{files}__ : open multiple files in tabs

Tabs
====
- *gt* : switch tab
- *tabf* __{file}__ : open file in new tab
- *tabdo* __{cmd}__ : run command through all tabs

Moving around
=============
- *%* : move to matching item (__(__, __)__, __{__, __}__, __[__, __]__...)
- *g*/*G* : jump to end/beginning of __file__
- *0*/*$* : jump to end/beginning of __line__
- *H*/*M*/*L* : move to top/middle/bottom of the screen

Panels
======
- *(v)sp(lit)* : split screen (vertically)/horizontally

BANG!
=====
Prefix by *:r* to paste the output. E.g.\
- *:r* __!__*wc* __%__ (current file)
- *:r* __!__*ls* (or __!__*pwd*)
- *:cd* /path


It can also be done after visually selecting some text : it is then piped to the cmd and replace the original content.\
- __!__*sort*


Formatting
==========
- __CTRL+q__ : comment/uncomment selection
- __\<select\>__+*u*/*U* : lowercase / uppercase selection - Alt: *guu*/*gUU* : lowercase / uppercase whole line
- __\<select\>__+__N__*>* : indent by tabs
- __\<select\>__+*:s/^/*+__N__*>* : indent by spaces
- *=* : auto (re)indent selection
- *=G* : auto (re)indent whole file

Substitution
============
- *:%s/*__regex__*/*__replacement__*/g* : global find & replace
- *:%g/*__regex__*/d* : delete all lines matching the pattern

Navigation
==========
- *:*__{line number}__ : goto line
- */* __regex__ : search pattern
- *n*/*N* : next/previous
- *\** : launch search with __regex__ = word under cursor

Edition
=========
- __TAB__ : autocomplete ; use __TAB__+__SPACE__ for real tabs, and __TAB__+__TAB__ to cancel completion
- *o*/*O* : insert mode on newline after/before current line
- *:ci"* or *ci<* or *ci(* : delete everything on the line in-between "..."/<...>/(...) and enter insert mode

Copy-paste
==========
- __F2__ : 'set paste' mode
- __SHIFT+INSERT__ : paste OS clipboard
- __CTRL+v__ : paste the clipboard
1. *v* : visual selection (or *q* for vertical selection)
2. *y*/*d* : copy (yank)/copy & delete
3. *p*/*P* : paste after/before
- *dd* : copy & delete line
- *yy* : copy line
- __"__+__+__+__y__ : copy line to system clipboard
- sometimes after a paste, vim keeps the whole document highlighted as if a "match-all" search had been triggered.
The solution: */* __some_dummy_pattern__

Registers
=========
- __0__ : only populated with yanked text  __"__+__0__+__p__
- __"__ (default) : also populated with text from *d*/*x*/*c*/*s* commands

Commands
========
- *:*__UP__ : commands history
- *:u* : undo
- __CTRL+r__ : redo
- *:.* : repeat last change - *:@* : repeat last command-line change

Config
======
- *:verbose set* __var__*?* : get config value
- *:[|i|n|v]map* : display current shortcuts / key bindings
- *:so %* : reload currently edited .vimrc
- *echo* os : get variable value

Display
=======
- **^M** : those are Windows newline
- *:set list* : show special characters
- *ga* : display ascii decimal, hex & octal value of character under cursor
- *:Ex* : file explorer (also __CTRL+x__ for NERDTree)
- *:ls* : list buffers (also *:BufExplorer*)

More tips
=========
- git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim && vim +PluginInstall +qall
- print to .ps with syntax coloring: *TERM=xterm-256color vim '+hardcopy >out.ps' +q src_file*
- gvim over ssh: grantm/bcvi
- *:set spell spelllang=fr* : enable vim 7.0+ spell checker. Then: *]s* / *]s* to navigate, *z=* for suggestions and *z=* to add to custom words list
- *vimtutor*
- *ggg?G* : rot13 whole file
- :help!  - :help 42  - :help bar  -  :help holy-grail  -  :Ni!

