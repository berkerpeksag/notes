# Merge Sort

Resources:

1. CLRS chapter 2
2. [https://www.youtube.com/watch?v=JPyuH4qXLZ0#t=17m11s](MIT Charles Leiserson
   video lecture on Merge Sort)

---

Define a recursive function that

1. divides an array in half
2. calls itself to sort both halves separately
3. merges the two resultant arrays after.

Once the two sorted halves have been shuffled together, return the resulting
array.


### Notes

* The average and worst-case time complexities of merge sort are `O(n log n)`.
* If you have a pre-processing check to see if the list is already sorted, you
  could have a best case of `O(n)`.
* Merge sort implementations are typically broken in to two distinct parts:
  1. a recursive `merge_sort` function,
  2. a simple array-merging `merge` function.
* Sorting, in general, takes at least `O(n log n)` time—the fastest sorting
  algorithm in existence that handles arbitrary data would take `O(n log n)`
  time.


### TODOs

* Explain what merge sort is and what to consider when implementing it.
* Write up your own implementation of merge sort.
* Write a function that merges an array of already sorted arrays, producing
  one large, still sorted array. For example, your input might be:

  ```
  [[0, 5, 8, 9], [1, 2, 7], [10]]
  ```

  And you should return:

  ```
  [0, 1, 2, 5, 7, 8, 9, 10]
  ```
* Look up how to do a merge sort in-place, without using any extra memory.
