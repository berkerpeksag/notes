# Learn C The Hard Way

## Types

* **Integers:** You declare integers with the `int` keyword, and print them with
  `%d`.
* **Floating Point:** Declared with `float` or `double` depending on how big
  they need to be (**double is bigger**), and printed with `%f`.
* **Character:** Declared with `char`, written with a `'` (single-quote)
  character around the char, and then printed with `%c`.

  ```c
  char initial = 'A';
  ```
* **String (Array of Characters):** Declared with `char name[]`, written with
  `"` characters, and printed with `%s`.

> **Note:** C makes a distinction between single-quote for `char` and
> double-quote for `char[]` or strings.

### Misc

#### Nul byte

```c
int bugs = 100;
/* Make a character, with a special syntax '\0' which creates a 'nul byte'
   character. This is effectively the number 0. */
char nul_byte = '\0';
int care_percentage = bugs * nul_byte;

printf("Which means you should care %d%%.\n", care_percentage);
```
