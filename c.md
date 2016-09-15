# Practical C Programming

* Local variables are temporary unless they are declared `static`.
* `static` has an entirely different meaning when used with global
  variables. It indicates that a variable is local to the current file.
* See for the `static` example: [/playground/practical-c/vars.c][varsc]

[varsc]: https://bitbucket.org/berkerpeksag/playground/src/32794b23c2ccc1e06de9af7992cbacfeb0533f78/practical-c/vars.c?at=master

# Learn C The Hard Way

## Types

* **Character:** Declared with `char`, written with a `'` (single-quote)
  character around the char, and then printed with `%c`.

  ```c
  char initial = 'A';
  ```
* **String (Array of Characters):** Declared with `char name[]`, written with
  `"` characters, and printed with `%s`.

> **Note:** C makes a distinction between single-quote for `char` and
> double-quote for `char[]` or strings.

## Misc

### Pointer analogy

```c
house_t my_house;  // a house
house_t *house_ptr;  // sign that says where some house is
// update house_ptr to point to my house. &my_house being the address of my house
house_ptr = &my_house;
```
([Source](https://www.reddit.com/r/C_Programming/comments/529uzo/for_anyone_who_is_having_issues_with_pointers_i/d7j6uxl))

### Nul byte

```c
int bugs = 100;
/* Make a character, with a special syntax '\0' which creates a 'nul byte'
   character. This is effectively the number 0. */
char nul_byte = '\0';
int care_percentage = bugs * nul_byte;

printf("Which means you should care %d%%.\n", care_percentage);
```

# Resources

## Compilations

* http://c-faq.com/

## Articles

* http://eli.thegreenplace.net/2008/07/18/reading-c-type-declarations/
* http://stackoverflow.com/questions/840501/how-do-function-pointers-in-c-work/
* http://stackoverflow.com/questions/897366/how-do-pointer-to-pointers-work-in-c/897414#897414
