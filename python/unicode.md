In Python 2

* **unicode.encode()** -> bytes
* **str.decode()** -> unicode

**Example:**

```py
>>> my_unicode = u"Hi \u2119\u01b4\u2602\u210c\xf8\u1f24"
>>> len(my_unicode)
9  # 9 codepoints
>>> my_utf8 = my_unicode.encode('utf-8')
>>> len(my_utf8)
19  # 19 bytes
>>> my_utf8
'Hi \xe2\x84\x99\xc6\xb4\xe2\x98\x82\xe2\x84\x8c\xc3\xb8\xe1\xbc\xa4'
>>> my_utf8.decode('utf-8')
u'Hi \u2119\u01b4\u2602\u210c\xf8\u1f24'
```

---

In Python 2 there are two basic string types: `str` and `unicode`. `str` may
carry encoded unicode data but it's always represented in bytes whereas the
unicode type does not contain bytes but charpoints. What does this mean? Imagine
you have the German Umlaut *ö*. In ASCII you cannot represent that character,
but in the latin-1 and UTF-8 character sets you can represent it, but they look
differently when encoded:

```py
>>> u'ö'.encode('latin1')
'\xf6'
>>> u'ö'.encode('utf-8')
'\xc3\xb6'
```

So an *ö* might look totally different depending on the encoding which makes it
hard to work with it. The solution is using the `unicode` type (as we did above,
note the `u` prefix before the string). The `unicode` type does not store the
bytes for *ö* but the information, that this is a `LATIN SMALL LETTER O WITH
DIAERESIS`.

Doing `len(u'ö')` will always give us the expected *"1"* but `len('ö')` might
give different results depending on the encoding of `'ö'`.
