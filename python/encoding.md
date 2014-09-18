# Encoding

### Glossary

#### Character Set

* A Character Set is a collection of elements used to represent textual
 information.
* Most of the Character Sets assign a number to each element - they are
  also known as Coded Character Sets.

#### `ISO-8859-*` Family

* 1 Western European
* 2 Central European
* 3 South European
* 4 North European
* 5 Latin/Cyrillic
* 6 Latin/Arabic
* 7 Latin/Greek
* 8 Latin/Hebrew
* 9 Turkish
* 10 Nordic
* 11 Latin/Thai
* 13 Baltic Rim
* 14 Celtic
* 15 Western European 2
* 16 South-Eastern European

#### Quick Intro to Unicode

* Unicode covers all the characters for all the writing systems of the
  world, modern and ancient.
* Unicode provides a unique number for every character
  - no matter what the platform
  - no matter what the program
  - no matter what the language
* The number is called "codepoint".
* 1114112 different codepoints
  - `U+0000` to `U+10FFFF`
* Replaces hundreds of existing character sets

#### Codepoints

* An integer in the range from `0` to `10FFFF`
* Expressed with the notation `U+XXXX`
* For example 'a' → `U+0061`, 'ä' → `U+00E4`
* Each Unicode character (e.g. ☃) has:
  - a codepoint (e.g. `U+2603`)
  - a name (e.g. SNOWMAN)
  - a category (e.g. So - Symbol, Other)
  - a block (e.g. Miscellaneous Symbols)
  - and other attributes

#### Unicode Planes

* Unicode is organized in 16 planes, with 65536 codepoints each
* Basic Multilingual Plane (BMP): includes most of the commonly used
  characters
* Supplementary Planes (non-BMP)

---

Files don't contain text, they contain bytes. Bytes only become text when
filtered through the correct encoding.

Python should not guess the encoding if it's unknown. Without the right
encoding, you don't get text, you get partial or complete gibberish.

So, if what you want is to parse text and not get gibberish, you need to
*tell* Python what the encoding is. That's a brute fact of the world of
text in computing.

Reference: https://mail.python.org/pipermail/python-dev/2014-January/131050.html

---

The integer that in English is written as 100 is represented in memory
as bytes 0x0064 (assuming a big-endian C short), so when you say "an
integer is written down AS-IS" (emphasis added), to me that says that
the PDF file includes the bytes 0x0064. But then you go on to write the
three character string "100", which (assuming ASCII) is the bytes
0x313030. Going from the C short to the ASCII representation 0x313030 is
nothing like inserting the int "as-is". To put it another way, the
Python 2 '%d' format code does not just copy bytes.

Reference: https://mail.python.org/pipermail/python-dev/2014-January/131191.html

---

### The rule of working with bytes

* work internally with Unicode text;
* convert to and from bytes only on input and output.

---

## Unicode Basics


* Python 3 always stores text strings as sequences of Unicode code points. These
  are values in the range `0-0x10FFFF`.
* To store text as binary data, you must specify an *encoding* for that text.
* The process of converting from a sequence of bytes (i.e. binary data) to a
  sequence of code points (i.e. text data) is *decoding*, while the reverse
  process is *encoding*.
* For historical reasons, the most widely used encoding is `ascii`, which can
  only handle Unicode code points in the range `0-0xEF` (i.e. ASCII is a 7-bit
  encoding).
* There are a wide variety of ASCII compatible *encodings*, which ensure that
  any appearance of a valid ASCII value in the binary data refers to the
  corresponding ASCII character.
* “utf-8” is becoming the preferred encoding for many applications, as it is an
  ASCII-compatible encoding that can encode any valid Unicode code point.
* “latin-1” is another significant ASCII-compatible encoding, as it maps byte
  values directly to the first 256 Unicode code points.
* There are also many ASCII incompatible encodings in widespread use,
  particularly in Asian countries (which had to devise their own solutions
  before the rise of Unicode) and on platforms such as Windows, Java and the
  .NET CLR, where many APIs accept text as UTF-16 encoded data.
* The `locale.getpreferredencoding()` call reports the encoding that Python will
  use by default for most operations that require an encoding (e.g. reading in a
  text file without a specified encoding). This is designed to aid
  interoperability between Python and the host operating system, but can cause
  problems with interoperability between systems (if encoding issues are not
  managed consistently).
* The `sys.getfilesystemencoding()` call reports the encoding that Python will
  use by default for most operations that both require an encoding and involve
  textual metadata in the filesystem (e.g. determining the results of
  `os.listdir()`)
* If you’re a native English speaker residing in an English speaking country
  it’s tempting to think “but Python 2 works fine, why are you bothering me with
  all this Unicode malarkey?”. It’s worth trying to remember that we’re actually
  a minority on this planet and, for most people on Earth, ASCII and `latin-1`
  can’t even handle their name, let alone any other text they might want to
  write or process in their native language.

Reference: http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html#unicode-basics


## Automatic encoding detection

There's a simple "guess the encoding of text files" heuristic which uses the
presence of a BOM to pick the encoding:

- read the first four bytes in binary mode
- if bytes 0 and 1 are FEFF or FFFE, then the encoding is UTF-16;
- if bytes 0 through 2 are EFBBBF, then the encoding is UTF-8;
- if bytes 0 through 3 are 0000FEFF or FFFE0000, then the encoding
  is UTF-32;
- if bytes 0 through 2 are 2B2F76 and byte 3 is 38, 39, 2B or 2F,
  then the encoding is UTF-7;
- otherwise the encoding is unknown.

Reference: https://mail.python.org/pipermail/python-dev/2014-January/131481.html


## General Encoding Notes

* Encoding is simply the process of transforming information from one format
  into another.
* ASCII was created so that everything English (and the unprintable stuff like
  spaces and linefeeds) could fit in 127 places, which took up just 7 bits
  (0-127).
* But since computers were using 8-bit bytes, various governments and groups
  started thinking up of things to do with the other 128 places (128-255). The
  problem is that they didn't agree on what to do with them, and chaos
  ensued. The result was that documents sent from system to system often could
  not be read because they were using different character standards.
* Finally, the IBM (OEM) and ANSI (Microsoft) systems were created, which
  defined code pages that consisted of ASCII for the bottom 127 characters and
  then a given language variation for the top 128 characters. So code pages 437
  (IBM), 737 (Greek), 862 (Turkish), etc., were all 256 characters each, with
  ASCII as the first 127 and then their respective language for the
  other 128. This way anyone using the same code page would be able to exchange
  documents without having his content mangled.

It's helpful to think of encoding methods as falling into two main
categories--the old way and the new way.

* The Old Way: Each character has a specific and direct representation on a
  computer.
* The New Way: Each character is a concept, and can be represented in multiple
  ways.

**The Old Way:** ASCII is one of the first types of encoding, and it uses the
old way. In other words, ASCII characters are stored in a fixed number of bits
in memory-all the time, every time. So an ASCII "D" always looks like this on a
computer:

    0100 0100

EBCDIC, ASCII, and code pages are all examples of this old system of mapping
directly to integers that are stored in a fixed way.

**The New Way:** The newer, better solution is to not map characters directly at
all, and to instead map them to a very specific conceptual entity which can
then be described by a computer in multiple ways (using more bits/bytes as
needed). This is what Unicode does--it maps every letter of every language to
a unique number (called a code point), so an upper-case "D" in Unicode maps to:

    U+0044

So now that you have set of individual numbers (code points) for characters you
can decide how to handle them using a computer. **This is the encoding part.**

Unicode and the Universal Character Set (UCS) are examples of the new system
that makes a distinction between identity and representation.

**The key distinction between the old way and the new way is that the old way
combined the characters themselves with how they were represented on a
computer, whereas the new system decouples these pieces.**

### ASCII

* This is a 7-bit system (0-127).
* Characters from 0-31 are non-printable, and from 32-127 are the standard
  characters that people often mistakenly call "plain text".

### Extended ASCII

* Any character system that has content between 128 and 256 in addition to 0-127
  is considered to be an implementation of extended ASCII. These include both
  code pages and Unicode.

### Unicode

* It was designed to replace code pages, which are various language-specific
  character mappings of 256 characters each.

### UTF-8/16/32

* Unicode has numerous ways of converting these code points into actual bits and
  bytes on a computer; these are called Unicode Transformation Formats (UTFs).
* The "8" in "UTF-8" doesn't indicate how many bits a code point gets encoded
  into. The final size of the encoded data is based on two things: a) the code
  unit size, and b) the number of code units used. So the 8 in UTF-8 stands for
  the code unit size, not the number of bits that will be used to encode a code
  point.

### UCS-4

* UCS-4 is identical, from a character mapping standpoint, to UTF-32. Both are
  fixed-length encoding schemes that encode every UCS/Unicode code point to 32
  bits.

### ISO 8859

* ISO 8859 is an early ISO standard (before UCS/Unicode) that attempted to unify
  code mapping systems.
* ISO 8559 is an 8 bit system that groups various alphabets into parts, which
  are then named 8859-1, 8859-2, etc.
* This standard is pretty much obsoleted by UCS/Unicode.

### Encoding FAQ

#### The relationship between Unicode and encodings like UTF-8

So,  say we have a string:

    Hello

which, in Unicode, corresponds to these five code points:

    U+0048 U+0065 U+006C U+006C U+006F.

Just a bunch of code points. Numbers, really. We haven't yet said anything about
how to store this in memory or represent it in an email message.

That's where *encodings* come in.

UTF-8 was another system for storing your string of Unicode code points, those
magic U+ numbers, in memory using 8 bit bytes. In UTF-8, every code point from
0-127 is stored in a single byte. Only code points 128 and above are stored
using 2, 3, in fact, up to 6 bytes.

This has the neat side effect that English text looks exactly the same in UTF-8
as it did in ASCII, so Americans don't even notice anything wrong.

Specifically, *Hello*, which was U+0048 U+0065 U+006C U+006C U+006F, will be
stored as 48 65 6C 6C 6F, which, behold! is the same as it was stored in ASCII,
and ANSI, and every OEM character set on the planet.

And in fact now that you're thinking of things in terms of platonic ideal
letters which are represented by Unicode code points, those unicode code points
can be encoded in any old-school encoding scheme, too! For example, you could
encode the Unicode string for Hello (U+0048 U+0065 U+006C U+006C U+006F) in
ASCII, or the old OEM Greek Encoding, or the Hebrew ANSI Encoding, or any of
several hundred encodings that have been invented so far, with one catch: some
of the letters might not show up! If there's no equivalent for the Unicode code
point you're trying to represent in the encoding you're trying to represent it
in, you usually get a little question mark: ? or, if you're really good, a
box. Which did you get? -> �

#### What's the difference between Unicode and UCS (ISO 10646)?

Think of Unicode and UCS as basically the same when it comes to character
mapping. They almost mirror each other in this regard. Unicode, however, adds a
number of features such as the ability to properly render right-to-left scripts,
perform string sorting and comparison, etc. If ever in doubt you probably want
to use Unicode.

#### Which schemes encode to which lengths?

* ASCII -> 7 bits
* "Extended ASCII" -> 8 bits
* UTF-7 -> 7 bits
* IBM (OEM) Code Maps -> 8 bits
* ANSI (Microsoft) Code Maps -> 8 bits
* ISO 8859 -> 8 bits
* UTF-8 -> 1-4 bytes
* UTF-16 -> 2-4 bytes
* UTF-32 -> 4 bytes
* UCS-2 -> 2 bytes (obsolete)
* UCS-4 -> 4 bytes

#### 7-bit ASCII vs. 8-bit ASCII

ASCII was originally conceived as a 7-bit code. This was done well before 8-bit
bytes became ubiquitous, and even into the 1990s you could find software that
assumed it could use the 8th bit of each byte of text for its own purposes ("not
8-bit clean").

There are dozens of text encodings that make use of the 8th bit; they can be
classified as ASCII-compatible or not, and fixed- or
variable-width. ASCII-compatible means that regardless of context, single bytes
with values from 0x00 through 0x7F encode the same characters that they would in
ASCII.

A fixed-width encoding means what it sounds like: all characters are encoded
using the same number of bytes. To be ASCII-compatible, a fixed-with encoding
must encode all its characters using only one byte, so it can have no more than
256 characters. The most common such encoding nowadays is Windows-1252, an
extension of ISO 8859-1.

There's only one variable-width ASCII-compatible encoding worth knowing about
nowadays, but it's very important: UTF-8, which packs all of Unicode into an
ASCII-compatible encoding.

"ASCII" nowadays takes its practical definition from Unicode, not its original
standard (ANSI X3.4-1968), because historically there were several dozen
variations on the ASCII 127-character repertoire.

Nowadays all of those variations are obsolescent, and when people say "ASCII"
they mean that the bytes with value 0x00 through 0x7F encode Unicode codepoints
U+0000 through U+007F.

**References**

1. http://www.danielmiessler.com/study/encoding/
2. http://stackoverflow.com/a/14690651
3. http://www.joelonsoftware.com/articles/Unicode.html
