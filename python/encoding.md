# Encoding

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
