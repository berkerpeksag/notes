Vim Cheatsheet
**************

Vim
===

Movement
--------

:f<char>:       jump to next occurance of <char>. Repeat with ``:``
:F<char>:       jump to previous occurance of <char>. Repeat with ``:``
:<number>G:     Go to line <number>
:H M L:         Go to top/middle/bottom of current screen
:zz:            Center current line
:CTRL-O:        Jump backward
:CTRL-I:        Jump forward
:( ):           Next / previous sentence
:{ }:           Next / previous paragraph

Marks
-----

:m<char>:       Create mark
:\`<char>:      Jump to mark
:'<char>:       Jump to line of mark

Editing
-------

:diw daw:       Delete word under cursor
:dis das:       Delete sentence under cursor
:dip dap:       Delete paragraph under cursor
:~:             Change case of the letter under cursor
:J:             Join lines

``:e!``
    Reset file
``:nohl``
    Reset highlighting
``:%s/search/replace/``
    Regex search replace whole file.
    Append g for multiple hits per line.
    Append c for interactive mode.
``:echo <name>``
    Output variable <name> e.g. $PYTHONPATH
``:let <name> = <value>``
    Set variable <name> to <value> (<value> must be variable or string)

Plugins
=======

Command T
---------

:<leader> t:    Start search

NERDTree
--------

:B:         Toggle Bookmarks
:C:         Change tree root to selected dir
:cd:        Set CWD to selected dir
:I:         Toggle hidden files
:m:         Show menu
:O:         Recursively open node
:R:         Refresh current root
:u:         Move tree root up a dir
:x:         Close parent of node

``:NERDTree``
    Open NERDTree window
``:Bookmark <name>``
    Bookmark the current node as <name>

