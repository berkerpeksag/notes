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
