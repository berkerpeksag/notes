# Unicode in Python 2

## Introduction to Unicode

### History of Character Codes

In 1968, ASCII was standardized. ASCII defined numeric codes for various
characters, with the numeric values running from `0` to `127`. For example, the
lowercase letter `a` is assigned `97` as its code value.

ASCII was an American-developed standard, so it only defined unaccented
characters. There was an `e`, but no `é` or `Í`. This meant that languages which
required accented characters couldn’t be faithfully represented in ASCII.
(Actually the missing accents matter for English, too, which contains words such
as ‘naïve’ and ‘café’, and some publications have house styles which require
spellings such as ‘coöperate’.)

In the 1980s, almost all personal computers were 8-bit, meaning that bytes could
hold values ranging from `0` to `255`. ASCII codes only went up to `127`, so
some machines assigned values between `128` and `255` to accented characters.
Different machines had different codes, however, which led to problems
exchanging files. Eventually various commonly used sets of values for the
`128-255` range emerged.

`255` characters aren’t very many. For example, you can’t fit both the accented
characters used in Western Europe and the Cyrillic alphabet used for Russian
into the `128-255` range because there are more than `127` such characters.

You could write files using different codes (all your Russian files in a coding
system called KOI8, all your French files in a different coding system called
Latin1), but what if you wanted to write a French document that quotes some
Russian text? In the 1980s people began to want to solve this problem, and the
Unicode standardization effort began.

Unicode started out using 16-bit characters instead of 8-bit characters. 16 bits
means you have `2^16=65,536` distinct values available, making it possible to
represent many different characters from many different alphabets; an initial
goal was to have Unicode contain the alphabets for every single human language.
It turns out that even 16 bits isn’t enough to meet that goal, and the modern
Unicode specification uses a wider range of codes, `0-1,114,111` (`0x10ffff` in
base-16).

### Definitions

#### Character

A character is the smallest possible component of a text. ‘A’, ‘B’, ‘C’, etc.,
are all different characters. So are ‘È’ and ‘Í’.

Characters are abstractions, and vary depending on the language or context
you’re talking about. For example, the symbol for ohms (Ω) is usually drawn much
like the capital letter omega (Ω) in the Greek alphabet (they may even be the
same in some fonts), but these are two different characters that have different
meanings.

#### Code points

The Unicode standard describes how characters are represented by code points. A
code point is an integer value, usually denoted in base 16. In the standard, a
code point is written using the notation `U+12ca` to mean the character with
value `0x12ca` (4810 in decimal). The Unicode standard contains a lot of tables
listing characters and their corresponding code points:

```
0061    'a'; LATIN SMALL LETTER A
0062    'b'; LATIN SMALL LETTER B
0063    'c'; LATIN SMALL LETTER C
...
007B    '{'; LEFT CURLY BRACKET
```

Strictly, these definitions imply that it’s meaningless to say ‘this is
character U+12ca’. `U+12ca` is a *code point*, which *represents* some
particular *character*; in this case, it represents the character
`ETHIOPIC SYLLABLE WI`. In informal contexts, this distinction between code
points and characters will sometimes be forgotten.

#### Glyph

A character is represented on a screen or on paper by a set of graphical
elements that’s called a glyph. The glyph for an uppercase A, for example, is
two diagonal strokes and a horizontal stroke, though the exact details will
depend on the font being used. Figuring out the correct glyph to display is
generally the job of a GUI toolkit or a terminal’s font renderer.

