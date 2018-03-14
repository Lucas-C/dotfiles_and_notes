" Author: Lucas Cimon (github.com/Lucas-C/linux_configuration)
if has("multi_byte")
  set encoding=utf-8
  setglobal fileencoding=utf-8
  "setglobal bomb
  set fileencodings=ucs-bom,utf-8,latin1
endif

"""UI
colorscheme default " darkblue
set number
syntax on                 " syntax highlighting
set listchars=eol:$,tab:>-,trail:~,extends:>,precedes:< " prefix tabs with a > and trails with ~

"Creates a group ExtraWhitespace
hi ExtraWhitespace ctermbg=red guibg=red
"Highlight trailing whitespaces
autocmd Syntax * syn match ExtraWhitespace /\s\+\%#\@<!$/

"""Status line
set laststatus=2          " always have status bar
set showcmd               " Show visual selection size
"FROM : https://wincent.com/wiki/Set_the_Vim_statusline
set statusline=%<\ %n:%f\ %m%r%y%=%-35.(line:\ %l\ of\ %L,\ col:\ %c%V\ (%P)%)

"""Indentation
set autoindent            " copy the indentation from the previous line, when starting a new line
set cindent               " C code indenting
set expandtab             " Get rid of tabs altogether and replace with spaces
set shiftwidth=4          " Set indention level to be the same as softtabstop
set smarttab
set softtabstop=4         " Why are tabs so big?  This fixes it
set tabstop=4

"""Other options
if exists("&autochdir")
  set autochdir
endif
set backspace=2           " allow backspacing over everything in insert mode
set bs=2                  " http://vimdoc.sourceforge.net/htmldoc/options.html#%27bs%27
set diffopt=filler,iwhite " keep files synced and ignore whitespace
set fo=croq               " http://vimdoc.sourceforge.net/htmldoc/change.html#fo-table
if exists("&foldcolumn")
  set foldcolumn=2        " set a column incase we need it
endif
if exists("&foldlevel")
  set foldlevel=0         " show contents of all folds
endif
if exists("&foldmethod")
  set foldmethod=indent   " use indent unless overridden
endif
set helpfile=$VIMRUNTIME/doc/help.txt
set hidden                " hide buffers instead of closing
set history=500           " keep 50 lines of command line history
set ignorecase            " Do case insensitive matching
set smartcase             " case-sensitive if search contains an uppercase character
set incsearch             " Incremental search
set linebreak             " This displays long lines as wrapped at word boundries
set magic                 " regexp behave as in grep
set matchtime=10          " Time to flash the brack with showmatch
set nobackup              " Don't keep a backup file
"set noswapfile              " this guy is really annoying sometimes
set nocompatible          " Use Vim defaults (much better!)
if exists("&fen")
  set nofen               " disable folds
endif
set notimeout             " i like to be pokey
set path+=.,..,../..,../../..,../../../..,/usr/include
set scrolloff=1           " dont let the curser get too close to the edge
set showmatch             " Show matching brackets.
set textwidth=0           " Don't wrap words by default
set ttimeout              " timeout on key-codes
set ttimeoutlen=100       " timeout on key-codes after 100ms
set virtualedit=block     " let blocks be in virutal edit mode
set whichwrap+=<,>,[,],h,l,~                 " arrow keys can wrap in normal and insert modes
set wildmenu              " This is used with wildmode(full) to cycle options
set wildmode=list:longest,full               " list all options, match to the longest
set wrap

"Suffixes that get lower priority when doing tab completion for filenames, i.e. files not likely to be edited or read
set suffixes=.bak,~,.swp,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc,.class
au BufNewFile,BufRead *.wsgi set filetype=python
au BufNewFile,BufRead *.inc set filetype=php
au BufNewFile,BufRead *.install set filetype=php
au BufNewFile,BufRead *.module set filetype=php

"Non-persistent history ? Check ~/.viminfo permissions
set viminfo='20,\"50         " read/write a .viminfo file, don't store more than 50 lines of registers

if has("win32") || has("win64")
    set directory=$TMP
else
    set directory=/tmp
end

"if &term =~ '^screen'
if !empty($TMUX)
    " tmux will send xterm-style keys when its xterm-keys option is on
    execute "set <xUp>=\e[1;*A"
    execute "set <xDown>=\e[1;*B"
    execute "set <xRight>=\e[1;*C"
    execute "set <xLeft>=\e[1;*D"
endif

if empty($TERM)
    " Useful in Docker containers (tested with Windows + Cmder)
    set t_kD=[3~
    set <PageUp>=[5~
    set <PageDown>=[6~
    set <Home>=[1~
    set <End>=[4~
endif

if !exists(":W")
    command W :execute ':silent w !sudo tee % > /dev/null' | :edit!
endif

map <C-s> :w<CR>

if has('mouse')
  set mouse=a
endif

set pastetoggle=<F2>         "http://vim.wikia.com/wiki/Toggle_auto-indenting_for_code_paste
"set wrapmargin=80           " When pasteing, use this, because textwidth becomes 0 ; wrapmargin inserts breaks if you exceed its value

let mapleader = "\\"

"Bind <C-v> to paste the clipboard
let os=substitute(system('uname'), '\n', '', '')
if os == 'Darwin' || os == 'Mac'
    nmap <C-v> :r!pbpaste<CR>
    imap <C-v> <esc>:r!pbpaste<CR>i
elseif os == 'Linux'
    nmap <C-v> :r!xclip -o<CR>
    imap <C-v> <esc>:r!xclip -o<CR>i
    "The leader should probably be configured depending on the keyboard,
    "I'm keeping this value for AZERTY kb for now
    let mapleader = "<"
end

"Remapping q to vertical visual block selection (that default to <C-v>)
:nnoremap q <C-v>

"When editing a file, make screen display the name of the file you are editing
function! SetTitle()
    if $TERM =~ "^screen"
        let l:title = 'vi: ' . expand('%:t')
        if (l:title != 'vi: __Tag_List__')
            let l:truncTitle = strpart(l:title, 0, 15)
            silent exe '!echo -e -n "\033k' . l:truncTitle . '\033\\"'
        endif
    endif
endfunction
" Run it every time we change buffers
autocmd BufEnter,BufFilePost * call SetTitle()

try
    set undodir=~/.vim/undodir
    set undofile
catch
endtry

"""Pretty printing with :hardcopy
set printfont=:h9
set printoptions=number:y,left:5pc

"""PLUGINS
if isdirectory($HOME."/.vim/bundle/Vundle.vim")
    filetype off                "required by Vundle
    set rtp+=~/.vim/bundle/Vundle.vim
    call vundle#begin()
    Plugin 'gmarik/vundle'

    Bundle 'scrooloose/nerdcommenter'
    map <C-q> <plug>NERDCommenterToggle

    Bundle 'jlanzarotta/bufexplorer'
    Bundle 'scrooloose/nerdtree'
    map <C-x> :NERDTreeToggle<CR>

    Bundle 'guns/vim-clojure-static'
    Bundle 'Glench/Vim-Jinja2-Syntax'
    Bundle 'plasticboy/vim-markdown'
    " disabled because of https://github.com/plasticboy/vim-markdown/issues/79
    let g:vim_markdown_folding_disabled=1

    " Require vim compiled with +python
    "Bundle 'klen/python-mode'
    "Bundle 'emgram769/vim-multiuser'

    " Annotations for git changes
    Bundle 'airblade/vim-gitgutter'

    "Bundle 'davidhalter/jedi-vim'
    Bundle 'ervandew/supertab'
    let g:SuperTabDefaultCompletionType = "context"
    "To force to omni: "<C-X><C-O>"
    set omnifunc=syntaxcomplete#Complete

    Plugin 'othree/html5.vim'

    "Bundle 'scrooloose/syntastic'
    Plugin 'vim-syntastic/syntastic'
    " To know what's going on :SyntasticInfo ; to invoke it manually :SyntasticCheck
    " JSLint: npm install jshint -g # Config example: https://github.com/jshint/jshint/blob/master/examples/.jshintrc
    let g:syntastic_javascript_checkers = ['jshint']
    let g:syntastic_python_checkers = ['python', 'pylint', 'pyflakes', 'pep8']
    let g:syntastic_aggregate_errors = 1

    Plugin 'fatih/vim-go'
    Plugin 'rust-lang/rust.vim'

    call vundle#end()
endif
filetype plugin indent on
