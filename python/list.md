## Performance Notes

The list object consists of two internal parts; one object header, and one
separately allocated array of object references. The latter is reallocated as
necessary.

The list has the following performance characteristics:

* The list object stores pointers to objects, not the actual objects themselves.
  The size of a list in memory depends on the number of objects in the list, not
  the size of the objects.
* The time needed to get or set an individual item is constant, no matter what
  the size of the list is (also known as “O(1)” behaviour).
* The time needed to append an item to the list is “amortized constant”;
  whenever the list needs to allocate more memory, it allocates room for a few
  items more than it actually needs, to avoid having to reallocate on each call
  (this assumes that the memory allocator is fast; for huge lists, the
  allocation overhead may push the behaviour towards O(n*n)).
* The time needed to insert an item depends on the size of the list, or more
  exactly, how many items that are to the right of the inserted item (O(n)). In
  other words, inserting items at the end is fast, but inserting items at the
  beginning can be relatively slow, if the list is large.
* The time needed to remove an item is about the same as the time needed to
  insert an item at the same location; removing items at the end is fast,
  removing items at the beginning is slow.
* The time needed to reverse a list is proportional to the list size (O(n)).
* The time needed to sort a list varies; the worst case is O(n log n), but
  typical cases are often a lot better than that.
