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

### Encodings

A Unicode string is a sequence of code points, which are numbers from `0` to
`0x10ffff`. This sequence needs to be represented as a set of bytes (meaning,
values from `0-255`) in memory.

The rules for translating a Unicode string into a sequence of bytes are called
an **encoding**.

The first encoding you might think of is an array of 32-bit integers. In this
representation, the string “Python” would look like this:

```
   P           y           t           h           o           n
0x50 00 00 00 79 00 00 00 74 00 00 00 68 00 00 00 6f 00 00 00 6e 00 00 00
   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
```

This representation is straightforward but using it presents a number of
problems.

1. It’s not portable; different processors order the bytes differently.
2. It’s very wasteful of space. In most texts, the majority of the code points
   are less than 127, or less than 255, so a lot of space is occupied by zero
   bytes. The above string takes 24 bytes compared to the 6 bytes needed for an
   ASCII representation. Increased RAM usage doesn’t matter too much (desktop
   computers have megabytes of RAM, and strings aren’t usually that large), but
   expanding our usage of disk and network bandwidth by a factor of 4 is
   intolerable.
3. It’s not compatible with existing C functions such as `strlen()`, so a new
   family of wide string functions would need to be used.
4. Many Internet standards are defined in terms of textual data, and can’t
   handle content with embedded zero bytes.

Encodings don’t have to handle every possible Unicode character, and most
encodings don’t. For example, Python’s default encoding is the `ASCII`
encoding. The rules for converting a Unicode string into the ASCII encoding are
simple; for each code point:

1. If the code point is `< 128`, each byte is the same as the value of the code
   point.
2. If the code point is `128 or greater`, the Unicode string can’t be
   represented in this encoding. (Python raises a `UnicodeEncodeError` exception
   in this case.)

Latin-1, also known as ISO-8859-1, is a similar encoding. Unicode code points
`0-255` are identical to the Latin-1 values, so converting to this encoding
simply requires converting code points to `byte` values; if a code point larger
than `255` is encountered, the string can’t be encoded into Latin-1.

**Note:** Encodings don’t have to be simple one-to-one mappings like Latin-1.
Consider IBM’s EBCDIC, which was used on IBM mainframes. Letter values weren’t
in one block: `a` through `i` had values from `129 to 137`, but `j` through `r`
were `145 through 153`. If you wanted to use EBCDIC as an encoding, you’d
probably use some sort of lookup table to perform the conversion, but this is
largely an internal detail.

UTF-8 is one of the most commonly used encodings. UTF stands for “Unicode
Transformation Format”, and the ‘8’ means that 8-bit numbers are used in the
encoding. UTF-8 uses the following rules:


1. If the code point is `< 128`, it’s represented by the corresponding byte
   value.
2. If the code point is between `128` and `0x7ff`, it’s turned into two byte
   values between `128` and `255`.
3. Code points `> 0x7ff` (<= 2047) are turned into three- or four-byte sequences
   , where each byte of the sequence is between `128` and `255`.

UTF-8 has several convenient properties:

1. It can handle any Unicode code point.
2. A Unicode string is turned into a string of bytes containing no embedded zero
   bytes. This avoids byte-ordering issues, and means UTF-8 strings can be
   processed by C functions such as `strcpy()` and sent through protocols that
   can’t handle zero bytes.
3. **A string of ASCII text is also valid UTF-8 text.**
4. UTF-8 is *fairly* compact; the majority of code points are turned into two
   bytes, and values less than `128` occupy only a single byte.
5. If bytes are corrupted or lost, it’s possible to determine the start of the
   next UTF-8-encoded code point and resynchronize. It’s also unlikely that
   random 8-bit data will look like valid UTF-8.


## Python 2’s Unicode Support

### The Unicode Type

Unicode strings are expressed as instances of the `unicode` type.

```
        basestring
            |
           / \
         str unicode
```

Under the hood, Python represents Unicode strings as either 16- or 32-bit
integers, depending on how the Python interpreter was compiled.

The `unicode()` constructor has the signature
`unicode(string[, encoding, errors])`. All of its arguments should be 8-bit
strings. The first argument is converted to Unicode using the specified
encoding; if you leave off the encoding argument, the ASCII encoding is used for
the conversion, so characters greater than `127` will be treated as errors:

```py
>>> unicode('abcdef')
u'abcdef'
>>> s = unicode('abcdef')
>>> type(s)
<type 'unicode'>
>>> unicode('abcdef' + chr(255))
Traceback (most recent call last):
...
UnicodeDecodeError: 'ascii' codec can't decode byte 0xff in position 6:
ordinal not in range(128)
```

The errors argument specifies the response when the input string can’t be
converted according to the encoding’s rules. Legal values for this argument are
`strict` (raise a `UnicodeDecodeError` exception), `replace` (add `U+FFFD`,
`REPLACEMENT CHARACTER`), or `ignore` (just leave the character out of the
Unicode result). The following examples show the differences:

```py
>>> unicode('\x80abc', errors='strict')
Traceback (most recent call last):
    ...
UnicodeDecodeError: 'ascii' codec can't decode byte 0x80 in position 0:
ordinal not in range(128)
>>> unicode('\x80abc', errors='replace')
u'\ufffdabc'
>>> unicode('\x80abc', errors='ignore')
u'abc'
```

### Unicode Literals in Python Source Code

In Python source code, Unicode literals are written as strings prefixed with the
‘u’ or ‘U’ character: `u'abcdefghijk'`. Specific code points can be written
using the `\u` escape sequence, which is followed by four hex digits giving the
code point. The `\U` escape sequence is similar, but expects 8 hex digits,
not 4.

Unicode literals can also use the same escape sequences as 8-bit strings,
including `\x`, but `\x` only takes two hex digits so it can’t express an
arbitrary code point. Octal escapes can go up to U+01ff, which is octal 777.

```py
>>> s = u"a\xac\u1234\u20ac\U00008000"
... #      ^^^^ two-digit hex escape
... #          ^^^^^^ four-digit Unicode escape
... #                      ^^^^^^^^^^ eight-digit Unicode escape
>>> for c in s:  print ord(c),
...
97 172 4660 8364 32768
```
