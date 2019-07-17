import sys


def utf8(s):
    s = ord(s)
    b = bytearray()
    if s < 0x80:
        b.append(s)
    elif s < 0x800:
        b.append(0xC0 | (s >> 6))
        b.append(0x80 | (s & 0x3F))
    elif s < 0x10000:
        b.append(0xE0 | (s >> 12))
        b.append(0x80 | (s >> 6 & 0x3F))
        b.append(0x80 | (s & 0x3F))
    elif s < 0x200000:
        b.append(0xF0 | (s >> 18))
        b.append(0x80 | (s >> 12 & 0x3F))
        b.append(0x80 | (s >> 6 & 0x3F))
        b.append(0x80 | (s & 0x3F))
    return b


def convert(s):
    sys.stdout.buffer.write(b''.join(map(utf8, s)) + b'\n')


convert('aışğ')
