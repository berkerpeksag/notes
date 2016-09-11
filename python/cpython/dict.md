# History of `dictobject.c`

**Note:** This is not complete yet.

My notes from
https://www.buzzfeed.com/andrewkelleher/deep-exploration-into-python-lets-review-the-dict-module.

**Discussions:**

* https://www.reddit.com/r/Python/comments/51oyh2/deep_exploration_into_python_lets_review_the_dict/

## API changes

* `d.values()`, `d.keys()`, `d.items()`: May 19, 1993
* `d.clear()`: March 21, 1997
* `d.copy()`: May 28, 1997
* `d.merge()`, `d.update()`: June 2, 1997
* `d.pop()`: October 6, 1997
* `d.first()`: November 30, 2000
* `d.popitem()`: December 12, 2000
* `for k in d`: April 20, 2001
* `key in d`, `key not in d`: April 20, 2001
* `d.iterkeys()`, `d.iteritems()`, `d.itervalues()`: May 1, 2001
* `d1 != d2`, `d1 == d2`: May 8, 2001
* `dict(['foo', 'bar'])`: October 26, 2001


## Glassary

* hash: a numeric value a key is mapped to by a hashing algorithm.
  In other words; `f(key)` -> `hash`
* slot: an empty position in the hash table a dictionary key-value can
  possibly be saved to
* dummy key: when a key-value is deleted from a dictionary, we don’t
  leave behind an empty slot. This would make it impossible to find
  other keys (we’ll go into that later). We leave behind a dummy instead.
* `NULL` keys: the value a key has before a slot in the table is
  used/occupied by a key-value pair
* entry: a hash and a key-value pair occupying a slot


## `mappingobject` and `mappingentry`

```c
typedef struct {
    OB_HEAD
    int ma_fill;
    int ma_used;
    int ma_size;
    mappingentry *ma_table;
} mappingobject;
```

[Source](https://github.com/python/cpython/blob/50eefde432319edd1b2b659278a01baa872ef22f/Objects/dictobject.c#L71)

```c
typedef struct {
    long me_hash;
    object *me_key;
    object *me_value;
} mappingentry;
```

[Source](https://github.com/python/cpython/blob/50eefde432319edd1b2b659278a01baa872ef22f/Objects/dictobject.c#L57)

The mapping object is a container for mapping entry(s). It maintains a
reference to

* `ma_fill` (the number of non-NULL keys — i.e., dummy keys + entries);
* `ma_used` (the number of non-NULL, non-dummy keys);
* and `ma_size`, a prime number representing the size (memory allocated)
  of the underlying table.

At the core of Python’s lookup algorithm is a method called “lookmapping.”
Guido describes it in his commit as:

> The basic lookup function used by all operations. This is essentially
> Algorithm D from Knuth Vol. 3, Sec. 6.4. Open addressing is preferred
> over chaining since the link overhead for chaining would be substantial.

**`lookmapping` implementation:**

```c
static mappingentry *lookmapping PROTO((mappingobject *, object *, long));
static mappingentry *
lookmapping(mp, key, hash)
    register mappingobject *mp;
    object *key;
    long hash;
{
    register int i, incr;
    register unsigned long sum = (unsigned long) hash;
    register mappingentry *freeslot = NULL;
    /* We must come up with (i, incr) such that 0 <= i < ma_size
       and 0 < incr < ma_size and both are a function of hash */
    i = sum % mp->ma_size;
    do {
        sum = sum + sum + sum + 1;
        incr = sum % mp->ma_size;
    } while (incr == 0);
    for (;;) {
        register mappingentry *ep = &mp->ma_table[i];
        if (ep->me_key == NULL) {
            if (freeslot != NULL)
                return freeslot;
            else
                return ep;
        }
        if (ep->me_key == dummy) {
            if (freeslot != NULL)
                freeslot = ep;
        }
        else if (ep->me_hash == hash &&
             cmpobject(ep->me_key, key) == 0) {
            return ep;
        }
        i = (i + incr) % mp->ma_size;
    }
}
```

[Reference](https://github.com/python/cpython/blob/50eefde432319edd1b2b659278a01baa872ef22f/Objects/dictobject.c#L121)

**`lookmapping` implementation v2:**

```c
static mappingentry *lookmapping PROTO((mappingobject *, object *, long));
static mappingentry *
lookmapping(mp, key, hash)
    mappingobject *mp;
    object *key;
    long hash;
{
    /* Optimizations based on observations by Jyrki Alakuijala
       (paraphrased):
       - This routine is very heavily used, so should be AFAP
       (As Fast As Possible).
       - Most of the time, the first try is a hit or a definite
       miss; so postpone the calculation of incr until we know the
       first try was a miss.
       - Write the loop twice, so we can move the test for
       freeslot==NULL out of the loop.
       - Write the loop using pointer increments and comparisons
       rather than using an integer loop index.
       Note that it behooves the compiler to calculate the values
       of incr*sizeof(*ep) outside the loops and use this in the
       increment of ep.  I've reduced the number of register
       variables to the two most obvious candidates.
       */

    register mappingentry *ep;
    mappingentry *end;
    register object *ekey;
    mappingentry *freeslot;
    unsigned long sum;
    int incr;
    int size;

    ep = &mp->ma_table[(unsigned long)hash%mp->ma_size];
    ekey = ep->me_key;
    if (ekey == NULL)
        return ep;
    if (ekey == dummy)
        freeslot = ep;
    else if (ep->me_hash == hash && cmpobject(ekey, key) == 0)
        return ep;
    else
        freeslot = NULL;

    size = mp->ma_size;
    sum = hash;
    do {
        sum = 3*sum + 1;
        incr = sum % size;
    } while (incr == 0);

    end = mp->ma_table + size;

    if (freeslot == NULL) {
        for (;;) {
            ep += incr;
            if (ep >= end)
                ep -= size;
            ekey = ep->me_key;
            if (ekey == NULL)
                return ep;
            if (ekey == dummy) {
                freeslot = ep;
                break;
            }
            if (ep->me_hash == hash && cmpobject(ekey, key) == 0)
                return ep;
        }
    }

    for (;;) {
        ep += incr;
        if (ep >= end)
            ep -= size;
        ekey = ep->me_key;
        if (ekey == NULL)
            return freeslot;
        if (ekey != dummy &&
            ep->me_hash == hash && cmpobject(ekey, key) == 0)
            return ep;
    }
}
```

[Reference](https://github.com/python/cpython/commit/99304174680d4c724476dad300ae7fc638842bf0)

**`lookmapping` implementation v3:**

```c
static mappingentry *lookmapping PROTO((mappingobject *, object *, long));
static mappingentry *
lookmapping(mp, key, hash)
    mappingobject *mp;
    object *key;
    long hash;
{
    register int i;
    register unsigned incr;
    register unsigned long sum = (unsigned long) hash;
    register mappingentry *freeslot = NULL;
    register int mask = mp->ma_size-1;
    register mappingentry *ep = &mp->ma_table[i];
    /* We must come up with (i, incr) such that 0 <= i < ma_size
       and 0 < incr < ma_size and both are a function of hash */
    i = (~sum) & mask;
    /* We use ~sum instead if sum, as degenerate hash functions, such
       as for ints <sigh>, can have lots of leading zeros. It's not
       really a performance risk, but better safe than sorry. */
    ep = &mp->ma_table[i];
    if (ep->me_key == NULL)
        return ep;
    if (ep->me_key == dummy)
        freeslot = ep;
    else if (ep->me_key == key ||
         (ep->me_hash == hash && cmpobject(ep->me_key, key) == 0)) {
        return ep;
    }
    /* Derive incr from i, just to make it more arbitrary. Note that
       incr must not be 0, or we will get into an infinite loop.*/
    incr = i << 1;
    if (!incr)
        incr = mask;
    if (incr > mask) /* Cycle through GF(2^n)-{0} */
        incr ^= mp->ma_poly; /* This will implicitly clear the
                    highest bit */
    for (;;) {
        ep = &mp->ma_table[(i+incr)&mask];
        if (ep->me_key == NULL) {
            if (freeslot != NULL)
                return freeslot;
            else
                return ep;
        }
        if (ep->me_key == dummy) {
            if (freeslot == NULL)
                freeslot = ep;
        }
        else if (ep->me_key == key ||
             (ep->me_hash == hash &&
              cmpobject(ep->me_key, key) == 0)) {
            return ep;
        }
        /* Cycle through GF(2^n)-{0} */
        incr = incr << 1;
        if (incr > mask)
            incr ^= mp->ma_poly;
    }
}
```

[Reference](https://github.com/python/cpython/commit/9c97b78659267b5757ca102c86478445a824a875)

**Further reading:**

* Algorithm D from Knuth Vol. 3, Sec. 6.4
* https://en.wikipedia.org/wiki/Open_addressing
* https://en.wikipedia.org/wiki/Hash_table#Separate_chaining

In Open Addressing, we allocate our whole address space. This includes space
for all the entries we are able to insert directly into the space, as well as
those that find their slot through a sequence of collisions.

**Example:** The key ‘a’ hashes to 12416037344. Taking the modulo with the
table size (8), we find it falls into slot 0. What if we want to add ‘i’ now,
which would also map to slot 0? It’s as simple as jumping forward some number
of slots according to “incr.” In our case, incr is set to 3. Each key that
might collide with slot 0 will find its home n times incr away, where n is the
number of collisions that have occurred up to that point.

The scenario we’ve described here has O(1) lookups in the best case, and O(n)
in the worst.

The *incr* formula is `(3 * hash + 1) % table_size`.

In modern implementations of GCC and clang, you’ll find the modulo operation
is optimized. But once upon a time, it actually broke down to this formula:

```py
def mod(x, y):
    return x - y * (x / y)
```

...which is three operations in one. Wow! To get away from this and move
toward fewer, faster operations, Guido (with help from other contributors)
committed a new lookup algorithm implementing the Galois Field for randomized
lookups. This decreased the collision rate substantially. See the
"`lookmapping` implementation v3" section for details.

After the Galois Field, there were a series of minor changes to the
`lookmapping` method that resulted in a 100% speed improvement:

* https://github.com/python/cpython/commit/e28e383d8555b576a8a8a1b2428adedb76bfc6aa

  Summary of the commit:

  - Changed sequences of “if” statements to “if/else”;
  - postponed casting “hash” until it was needed; and
  - stored “hash” in a register instead of on the stack.
* https://github.com/python/cpython/commit/6fbf61b06eaa09dc0f321027605d695de5cdb2eb
* https://github.com/python/cpython/commit/81673fb5ca25e17a1c1b806c06b046669a566a88

**TODO:** Explain this section better.

## Notes

* Python uses a hash table to get O(1) lookups on randomly accessed keys. The
  other most common choice for mapping objects is the binary tree lookup.

  > Python’s dictionaries are implemented as resizable hash tables.
  > Compared to B-trees, this gives better performance for lookup
  > (the most common operation by far) under most circumstances,
  > and the implementation is simpler.

  **Algorithmic complexity comparison**

  ```rst
         | Hash Table   |   Red-Black Tree    |
  -------+--------------+---------------------+
  Space  | O(n) : O(n)  | O(n)     : O(n)     |
  Insert | O(1) : O(n)  | O(log n) : O(log n) |
  Fetch  | O(1) : O(n)  | O(log n) : O(log n) |
  Delete | O(1) : O(n)  | O(log n) : O(log n) |
         | avg  : worst | average  : worst    |
  ```

  [Taken from Programmers Stack Exchange](http://programmers.stackexchange.com/a/234807).
* The quality of a hash table implementation in many ways comes down to the
  quality of its collision resolution mechanism. If keys become too close
  together in the table, we end up with a situation called “clustering.”
