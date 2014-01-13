set autochdir
set autoindent            " always set autoindenting on
set backspace=2           " allow backspacing over everything in insert mode
set bs=2                  " http://vimdoc.sourceforge.net/htmldoc/options.html#%27bs%27
set cindent               " c code indenting
set diffopt=filler,iwhite " keep files synced and ignore whitespace
set expandtab             " Get rid of tabs altogether and replace with spaces
set fo=croq               " http://vimdoc.sourceforge.net/htmldoc/change.html#fo-table
set foldcolumn=2          " set a column incase we need it
set foldlevel=0           " show contents of all folds
set foldmethod=indent     " use indent unless overridden
set guioptions-=m         " Remove menu from the gui
set guioptions-=T         " Remove toolbar
set hidden                " hide buffers instead of closing
set history=50            " keep 50 lines of command line history
set ignorecase            " Do case insensitive matching
set incsearch             " Incremental search
set laststatus=2          " always have status bar
set linebreak             " This displays long lines as wrapped at word boundries
set matchtime=10          " Time to flash the brack with showmatch
set nobackup              " Don't keep a backup file
set nocompatible          " Use Vim defaults (much better!)
set nofen                 " disable folds
set notimeout             " i like to be pokey
set wrap
set number
set tabstop=4
set textwidth=0           " Don't wrap words by default
set ttimeout              " timeout on key-codes
set ttimeoutlen=100       " timeout on key-codes after 100ms
set ruler                 " the ruler on the bottom is useful
set scrolloff=1           " dont let the curser get too close to the edge
set shiftwidth=4          " Set indention level to be the same as softtabstop
set showcmd               " Show (partial) command in status line.
set showmatch             " Show matching brackets.
set smartindent
set smarttab
set softtabstop=4         " Why are tabs so big?  This fixes it
set virtualedit=block     " let blocks be in virutal edit mode
set wildmenu              " This is used with wildmode(full) to cycle options

"Longer Set options
set cscopequickfix=s-,c-,d-,i-,t-,e-,g-,f-   " useful for cscope in quickfix
set listchars=tab:>-,trail:-                 " prefix tabs with a > and trails with -
set tags+=./.tags,.tags,../.tags,../../.tags " set ctags
set whichwrap+=<,>,[,],h,l,~                 " arrow keys can wrap in normal and insert modes
set wildmode=list:longest,full               " list all options, match to the longest

set helpfile=$VIMRUNTIME/doc/help.txt
set guifont=Courier\ 10\ Pitch\ 10
set path+=.,..,../..,../../..,../../../..,/usr/include

" Suffixes that get lower priority when doing tab completion for filenames.
" These are files I am not likely to want to edit or read.
set suffixes=.bak,~,.swp,.o,.info,.aux,.log,.dvi,.bbl,.blg,.brf,.cb,.ind,.idx,.ilg,.inx,.out,.toc,.class

"Disabled options
"set list                    " Make tabs and trails explicit
"set noswapfile              " this guy is really annoyoing sometimes
"set wrapmargin=80           " When pasteing, use this, because textwidth becomes 0
" wrapmargin inserts breaks if you exceed its value
"set cscopeprg=~/bin/cscope  "set cscope bin path

"Set colorscheme.  This is a black background colorscheme
colorscheme default " darkblue

" viminfo options
" read/write a .viminfo file, don't store more than
" 50 lines of registers
set viminfo='20,\"50


"Set variables for plugins to use

"vimspell variables
"don't automatically spell check!
let spell_auto_type=""

" LargeFile.vim settings
" don't run syntax and other expensive things on files larger than NUM megs
let g:LargeFile = 100

"Turn on filetype plugins to automagically
"Grab commands for particular filetypes.
"Grabbed from $VIM/ftplugin
filetype plugin on
filetype indent on

"Turn on syntax highlighting
syntax on

"Map \e to edit a file from the directory of the current buffer
if has("unix")
    nmap <Leader>e :e <C-R>=expand("%:p:h") . "/"<CR>
else
    nmap <Leader>,e :e <C-R>=expand("%:p:h") . "\\"<CR>
endif

"Functions
fu! CscopeAdd() " Add Cscope database named .cscope.out
    let dir = getcwd()
    let savedir = getcwd()
    wh (dir != '/')
        let scopefile = dir . '/' . ".cscope.out"
        if filereadable(scopefile)
            exe "cs add " scopefile
            exe "cd " savedir
            return dir
        en
        cd ..
        let dir = getcwd()
    endw
    exe "cd " savedir
endf

"Adding mail as a spell checked type, only if in 7.0 >
if (v:version >= 700)
    au FileType mail set spell
endif

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


if has("win32") || has("win64")
    set directory=$TMP
else
    set directory=/tmp
end

"http://vim.wikia.com/wiki/Toggle_auto-indenting_for_code_paste
set pastetoggle=<F2>

command W :execute ':silent w !sudo tee % > /dev/null' | :edit!

map!  

set mouse=a

set listchars=eol:$,tab:>-,trail:~,extends:>,precedes:<
"to show whitespaces: :set list

"Bind <F3> to paste the clipboard
let os=substitute(system('uname'), '\n', '', '')
if os == 'Darwin' || os == 'Mac'
    nmap <F3> :r!pbpaste<CR>
    imap <F3> <esc>:r!pbpaste<CR>i
elseif os == 'Linux'
    nmap <F3> :r!xclip -o<CR>
    imap <F3> <esc>:r!xclip -o<CR>i
end

"clojure
au BufRead,BufNewFile *.clj set filetype=clojure
