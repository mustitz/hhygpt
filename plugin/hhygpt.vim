if !has("python3")
    echo "vim has to be compiled with +python3 to run this"
    finish
endif

if exists('g:hhygpt_plugin_loaded')
    finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:error_msg = ''

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import hhyvim
EOF

let g:hhygpt_plugin_loaded = 1

function! s:GPT(args)
    python3 hhyvim.entry(vim.eval('a:args'))
    if s:error_msg != ''
        echoerr s:error_msg
    endif
endfunction

command! -nargs=* GPT call <SID>GPT(<q-args>)
