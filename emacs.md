# Emacs Cheatsheet

* Toggling read-only mode in a buffer: `C-x C-q`
* Reload `.emacs` without restart: `M-x load-file`
* Select all: `C-x h`
* Cursorun önündeki ifadeyi çalıştırıp, sonucunu minibuffer'da gösterir: `M-C-x`
* \*scratch\* bufferında cursor'un önündeki ifadeyi çalıştırmak için(sonuç
  ifadenin hemen altında çıkar): `C-j`
* Bufferlar için dosya arama benzeri(`C-x C-f`) finder: `C-x b`
* Yorum satırı yazarken bir alttaki satırdan devam etmek için `M-j`:
  ```el
  ;; ilk satır (press M-j)
  ;; ikinci satır
  ```
* Plcing the cursor just after the last closing paren: `C-x C-e`

## Help

* Get description of the major mode: `C-h m`
* Get all available keybindings grouped by modes: `C-h b`

## Buffers

* Split window horizontally: `C-x 3`
* Split buffer: `M-4`
* Switch cursor to other buffer: `M-5`
* Delete current buffer: `M-4`
* Expand current buffer: `M-5`
* Previous *user* buffer: `C-PageUp`
* Next *user* buffer: `C-PageDown`

## Search

* Incremental search: Next result `C-s`, previous result `C-r`
* Aramaya başladığım satıra geri dönmek: `C-v C-<SPACE>`

## Misc

* To make the region into comment or uncomment: `C-Space M-;`
* Speedbar: `M-x speedbar`
