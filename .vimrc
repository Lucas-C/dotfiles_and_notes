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
set autochdir
set backspace=2           " allow backspacing over everything in insert mode
set bs=2                  " http://vimdoc.sourceforge.net/htmldoc/options.html#%27bs%27
set diffopt=filler,iwhite " keep files synced and ignore whitespace
set fo=croq               " http://vimdoc.sourceforge.net/htmldoc/change.html#fo-table
set foldcolumn=2          " set a column incase we need it
set foldlevel=0           " show contents of all folds
set foldmethod=indent     " use indent unless overridden
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
set nocompatible          " Use Vim defaults (much better!)
set nofen                 " disable folds
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

"set noswapfile              " this guy is really annoying sometimes
"set wrapmargin=80           " When pasteing, use this, because textwidth becomes 0 ; wrapmargin inserts breaks if you exceed its value

"Non-persistent history ? Check ~/.viminfo permissions
set viminfo='20,\"50         " read/write a .viminfo file, don't store more than 50 lines of registers

if has("win32") || has("win64")
    set directory=$TMP
else
    set directory=/tmp
end

command W :execute ':silent w !sudo tee % > /dev/null' | :edit!

map!  

set mouse=a

set pastetoggle=<F2>         "http://vim.wikia.com/wiki/Toggle_auto-indenting_for_code_paste

let mapleader = "\\"

"Bind <F3> to paste the clipboard
let os=substitute(system('uname'), '\n', '', '')
if os == 'Darwin' || os == 'Mac'
    nmap <F3> :r!pbpaste<CR>
    imap <F3> <esc>:r!pbpaste<CR>i
elseif os == 'Linux'
    nmap <F3> :r!xclip -o<CR>
    imap <F3> <esc>:r!xclip -o<CR>i
    if system("setxkbmap -print") =~ "fr(UnicodeExpert)"
        let mapleader = "<"
    endif
end

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


"""PLUGINS
if isdirectory($HOME."/.vim/bundle/vundle")
    filetype off                "required
    set rtp+=~/.vim/bundle/vundle/
    call vundle#rc()
    Plugin 'gmarik/vundle'

    Plugin 'vim-scripts/LargeFile'
    let g:LargeFile = 100       "Large files are those with size > 100Mo
    set lazyredraw              "Don't redraw while executing macros (good performance config)

    Bundle 'scrooloose/nerdcommenter'
    map <leader>cc <plug>NERDCommenterAlignLeft
    map <leader>cb <plug>NERDCommenterComment

    Bundle 'jlanzarotta/bufexplorer'
    Bundle 'scrooloose/nerdtree'
    map <leader>nn :NERDTreeToggle<cr>

    Bundle 'guns/vim-clojure-static'
    Bundle 'JuliaLang/julia-vim'
    Bundle 'plasticboy/vim-markdown'
    let g:vim_markdown_initial_foldlevel=1
    Bundle 'scrooloose/syntastic'

    " require vim compiled with +python
    "Bundle 'klen/python-mode'
    "Bundle 'emgram769/vim-multiuser'

    " annotations for git changes
    Bundle 'airblade/vim-gitgutter'

    Bundle 'ervandew/supertab'
    let g:SuperTabDefaultCompletionType = "context"
    "To force to omni: "<C-X><C-O>"
    set omnifunc=syntaxcomplete#Complete
endif " Vundle END
filetype plugin indent on

