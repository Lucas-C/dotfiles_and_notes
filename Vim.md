% VIM_CHEAT_SHEET

Crashes
=======
- *vim -r* __file.swp__ : restore file

Files
=====
- *:w* __new_filename__ : save a copy and keep working on original

Moving around
=============
- *%* : move to matching item (__(__, __)__, __{__, __}__, __[__, __]__...)
- *g*/*G* : jump to end/beginning of __file__
- *0*/*$* : jump to end/beginning of __line__
- *H*/*M*/*L* : move to top/middle/bottom of the screen

Panels
======
- *(v)sp(lit)* : split screen (vertically)/horizontally

Tabs
====
- *vim -p* __{files}__
- *gt* : switch tab
- *tabf* __{file}__ : open file in new tab
- *tabdo* __{cmd}__ : run command through all tabs

BANG!
=====
Preffix by *:r* to paste the output.\
- *:r* __!__*ls*
- *:r* __!__*pwd*
- *:r* __!__*wc* __%__ (current file)
- *:cd* /path


It can also be done after visually selecting some text : it is then piped to the cmd and replace the original content.\
- __!__*sort*


Formatting
==========
- __\<leader>__cc : comment toggle selection
- *guu*/*gUU*/*~* : lowercase line / uppercase linei / invert case of selection
- __\<select\>__+__{tabs count}__*>* : indent
- *=* : auto (re)indent selection
- *=G* : auto (re)indent whole file

Substitution
============
- *:%s/*__regex__*/*__replacement__*/g* : global find & replace

Navigation
==========
- *:*__{line number}__ : goto line
- */* __regex__ : search pattern
- *n*/*N* : next/previous
- *\** : launch search with __regex__ = word under cursor

Insertion
=========
- __TAB__ : autocomplete
- __F2__ : 'set paste' mode
- *o*/*O* : insert mode on newline after/before current line

Copy-paste
==========
1. *v* : visual selection (or __CTRL__+V for vertical selection)
2. *y*/*d* : copy (yank)/copy & delete
3. *p*/*P* : paste after/before
- *dd* : copy & delete line
- *yy* : copy line
- __["]__+__[+]__+__[Y]__ : copy line to system clipboard

Registers
=========
- __[0]__ : only populated with yanked text  __["]__+__[0]__+__[p]__
- __["]__ (default) : also populated with text from *d*/*x*/*c*/*s* commands

Commands
========
- *:*__[UP]__ : commands history
- *:u* : undo
- __[CTRL]+[R]__ : redo
- *:.* : repeat

Config
======
- *:verbose set* __var__*?* : get config value
- *echo* os : get variable value

Display
=======
- **^M** : those are Windows newline
- *ga* : display ascii decimal, hex & octal value of character under cursor
- *:set list* : show special characters
- *:Ex* : file explorer (also __\<leader>__nn for NERDTree)
- *:ls* : list buffers (also __\<leader>__be for bufexplorer)

More tips
=========
- *vimtutor*
- *ggg?G* : rot13 whole file
- :help!  - :help 42  - :help bar  -  :help holy-grail  -  :Ni! 

