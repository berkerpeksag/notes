# color-theme vs. deftheme

Emacs 24 ile birlikte tema geliştirmek epey kolaylaştı ancak Emacs 23 ve
öncesinde color-theme ile geliştirilen temaları yeni yapıya port ederken
birkaç noktaya dikkat etmek gerekiyor.

Mesela color-theme ile yazdığımız temamız böyleydi:

```el
(defun bakunin ()
  (interactive)
  (color-theme-install
   '(bakunin
     ((background-color . "#000509")
      (foreground-color . "#FFFFFF")
      (background-mode . dark)
      (border-color . "#323232")
      (cursor-color . "#FFFFFF")
      (mouse-color . "#323232"))
     
     ;; Diger degisiklikler
     )))
```


