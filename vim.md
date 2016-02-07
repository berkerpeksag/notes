# Vim Notları

Son 2 yılımı çoğunlukla Emacs ve PyCharm ile geçiren biri olarak,
bir süre Vim kullanmaya karar verdim. Bu süre boyunca öğrendiklerimi
bu belgede toplayacağım.

## Sekmelerle Çalışmak

* Yeni sekme oluşturmak için `Ctrl-TAB`
* Sekmeler arasında gezinmek için **normal moddayken** `gt`
* Sırası belli bir sekmeye, örneğin 3. sekmeye gitmek istiyorsak `3gt`

## Genel Kısayollar

* Normal mode: `ESC` ya da `jj`
* Insert mode: `i`
* Undo: `u`
* Redo: `Ctrl-R`
* Bufferlar arasında gezinmek için `Ctrl+6`
* `dG` will delete from the current line to the end of file
* To go to first line of file, type `gg`
* To go to end of file, type `G`
* Type `gq` (and use `move up` or `move down`) to emulate `fill-paragraph`
* Duplicate a line: `Y` and `P`
* Go to line: `42G`
* Delete a word: `dw`
* Repeat the last change: `.`
* Delete the character under the cursor: `x`
* Delete the whole line: `dd`
* Move cursor to end of the line and switch to insert mode: `A`
* Move cursor to end of the line, switch to insert mode and press `<CR>`: `o`

## Searching

* `/pattern`: search forward for pattern
* `?pattern`: search backward
* `n`: repeat forward search
* `N`: repeat backward
* `:%s/search_for_this/replace_with_this/`: search whole file and replace
* `:%s/search_for_this/replace_with_this/c`: confirm each replace

## Bağlantılar

* http://vimhelp.appspot.com/vim_faq.txt.html
* Vim Tips: http://vim.wikia.com/wiki/Vim_Tips_Wiki
* http://www.catswhocode.com/blog/100-vim-commands-every-programmer-should-know
* http://lucumr.pocoo.org/2010/7/29/sharing-vim-tricks/
* https://www.cs.swarthmore.edu/help/vim/searching.html

### Plugin Yazmak

* Learn Vimscript the Hard Way: http://learnvimscriptthehardway.stevelosh.com/
* http://stevelosh.com/blog/2011/09/writing-vim-plugins/
* http://vim.wikia.com/wiki/How_to_write_a_plugin
