# Bitwise operation

`10000000` is 128, and `00000001` is 1.

```python
print int('10000000', 2)  # Output is 128
print int('00000001', 2)  # Output is 1
```

## `&` operator

The binary `&` operator returns a 1-bit if the two input bits are both 1.

```python
>>> print 0 & 0, 1 & 0, 1 & 1, 0 & 1
0 0 1 0
```

Here's the same kind of example, combining sequences of bits. This takes a bit
of conversion to base 2 to understand what's going on.

```python
>>> print 3 & 5
1
```

The number 3, in base 2, is `0011`. The number 5 is `0101`. Let's match up the
bits from left to right:

```
  0 0 1 1
& 0 1 0 1
  -------
  0 0 0 1
```

## `^` operator

The binary `^` operator returns a 1-bit if one of the two inputs are 1 but not
both. This is sometimes called the *exclusive or* or *XOR*.

```python
>>> print 3 ^ 5
6
```

```
  0 0 1 1
^ 0 1 0 1
  -------
  0 1 1 0
```

## `|` operator

The binary `|` operator returns a 1-bit if either of the two inputs is 1. This
is sometimes called the *inclusive or*. Sometimes this is written *and/or*.

```python
>>> print 3 | 5
7
```

```
  0 0 1 1
| 0 1 0 1
  -------
  0 1 1 1
```

## Bit shifting operations

There are also bit shifting operations. These are mathematically equivalent to
multiplying and dividing by powers of two. Often, machine hardware can execute
these operations faster than the equivalent multiply or divide.

### `<<` left-shift operator

The left argument is the bit pattern to be shifted, the right argument is the
number of bits.

```python
>>> print 0xA << 2
40
```

`0xA` is hexadecimal; the bits are `1010`. This is 10 in decimal. When we shift
this two bits to the left, it's like multiplying by 4. We get bits of `101000`.
This is 40 in decimal.

**Note:** Shifting left by `n` places is the same as multiplying by `2n`.

```c
int i, j;

j = 4;

i = j << 3; /* multiple j by 8 (2 ** 3)

/* slower than shift */
i = j * 8;
```

### `>>` right-shift operator

The left argument is the bit pattern to be shifted, the right argument is the
number of bits. Python always behaves as though it is running on a 2's
complement computer. The left-most bit is always the sign bit, so sign bits are
shifted in.

```python
>>> print 80 >> 3
10
```

The number 80, with bits of `1010000`, shifted right 3 bits, yields bits of
`1010`, which is 10 in decimal.
