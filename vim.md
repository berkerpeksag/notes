# Vim Notları

Son 2 yılımı çoğunlukla Emacs ve PyCharm ile geçiren biri olarak,
bir süre Vim kullanmaya karar verdim. Bu süre boyunca öğrendiklerimi
bu belgede toplayacağım.

## Sekmelerle Çalışmak

* Yeni sekme oluşturmak için `Ctrl-TAB`
* Sekmeler arasında gezinmek için **normal moddayken** `gt`
* Sırası belli bir sekmeye, örneğin 3. sekmeye gitmek istiyorsak `3gt`

## Vim Ayarları

* http://lucumr.pocoo.org/2010/7/29/sharing-vim-tricks/

## Genel Kısayollar

* Normal mode: `ESC`. Ayrıca `Ctrl-C` de kullanılabilir.
* Insert mode: `i`
* Undo: `u`
* Redo: `Ctrl-R`
* Bufferlar arasında gezinmek için `Ctrl+6`
* http://www.catswhocode.com/blog/100-vim-commands-every-programmer-should-know

## Nerdtree

### Kısayollar

* Use the natural vim navigation keys `hjkl` to navigate the files.
* Press `o` to open the file in a new buffer or open/close directory.
* Press `t` to open the file in a new tab.
* Press `i` to open the file in a new horizontal split.
* Press `s` to open the file in a new vertical split.
* Press `p` to go to parent directory.
* Press `r` to refresh the current directory.

Kaynak: http://www.catonmat.net/blog/vim-plugins-nerdtree-vim/

## Python

* https://github.com/klen/python-mode

### flake8

* Çalıştırmak için `F7`

## Linkler

* http://vimhelp.appspot.com/vim_faq.txt.html
* Vim Tips: http://vim.wikia.com/wiki/Vim_Tips_Wiki

## Vim Plugin Yazmak

* Learn Vimscript the Hard Way: http://learnvimscriptthehardway.stevelosh.com/
* http://stevelosh.com/blog/2011/09/writing-vim-plugins/
* http://vim.wikia.com/wiki/How_to_write_a_plugin
*
*## Vim Kaynak Kodu

Beklediğimden daha karman çorman ve Mercurial kullanımı rezalet. Google gibi
bit firmada çalışan Bram'in nasıl bu kadar kötü bir sürüm yönetim formatı
kurmayı becermiş çok merak ediyorum. Benim gibi Windows ile oyun oynama
haricinde işi olmayan biri için kodun büyük bölümü çöplük. Vim'e ve
Vimscript'e iyice hakim olduktan sonra, Windows bağımlılıklarını kaldırıp kodu
biraz daha temizlemek gibi bir hobi projem var.

Diğer hobi projeler:

* Pathogen üzerine bir package manager
* ~30 yıllık "man" belge formatı yerine Markdown kullanmak
  - Belki mevcut belgeleri Markdown'a çeviren bir betik yazılabilir.
