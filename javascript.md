# JavaScript Notes

## `var self = this;` workaround

One reason this question comes up so often is that function functions receive
a this value automatically, whether they want one or not. Have you ever
written this hack?

```js
{
  // ...
  addAll: function addAll(pieces) {
    var self = this;
    _.each(pieces, function (piece) {
      self.add(piece);
    });
  },
  // ...
}
```

Here, what you’d like to write in the inner function is just
`this.add(piece)`. Unfortunately, the inner function doesn’t inherit the outer
function’s `this` value. Inside the inner function, `this` will be `window` or
`undefined`. The temporary variable `self` serves to smuggle the outer value
of this into the inner function.

Another way is to use `.bind(this)` on the inner function.

Arrow functions do not have their own `this` value. The value of `this` inside
an arrow function is always inherited from the enclosing scope.

There’s one more minor difference between arrow and non-arrow functions: arrow
functions don’t get their own `arguments` object, either. Of course, in ES6,
you’d probably rather use a rest parameter or default value anyway.

In ES6, this hacks mostly go away if you follow these rules:

* Use non-arrow functions for methods that will be called using the
  `object.method()` syntax. Those are the functions that will receive a
  meaningful `this` value from their caller.
* Use arrow functions for everything else.

```js
// ES6
{
  ...
  addAll: function addAll(pieces) {
    _.each(pieces, piece => this.add(piece));
  },
  ...
}
```

In the ES6 version, note that the `addAll` method receives `this` from its
caller. The inner function is an arrow function, so it inherits `this` from
the enclosing scope.

---

As a bonus, ES6 also provides a shorter way to write methods in object
literals! So the code above can be simplified further:

```js
// ES6 with method syntax
{
  ...
  addAll(pieces) {
    _.each(pieces, piece => this.add(piece));
  },
  ...
}
```

**Reference:** https://hacks.mozilla.org/2015/06/es6-in-depth-arrow-functions/


## Promise

* http://www.html5rocks.com/en/tutorials/es6/promises/
* A simple promise implementation: http://www.mattgreer.org/articles/promises-in-wicked-detail/


## Falsy values

* `""`
* `0`, `-0`, `NaN`
* `null`, `undefined`
* `false`

Any value that's not on this "falsy" list is "truthy." Including `[]` and `{}`.

It's important to remember that a non-`boolean` value only follows this
"truthy"/"falsy" coercion if it's actually coerced to a `boolean`.

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#truthy--falsy


## The difference between `==` and `===`

The difference between `==` and `===` is usually characterized that `==` checks
for value equality and `===` checks for both value and type equality. However,
this is inaccurate. The proper way to characterize them is that `==` checks for
value equality with coercion allowed, and `===` checks for value equality
without allowing coercion; `===` is often called "strict equality" for this
reason.

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#equality


## When to use `==` and `===`

* If either value (aka side) in a comparison could be the `true` or `false`
  value, avoid `==` and use `===`.
* If either value in a comparison could be of these specific values (`0`, `""`,
  or `[]`), avoid `==` and use `===`.
* In all other cases, you're safe to use `==`. Not only is it safe, but in many
  cases it simplifies your code in a way that improves readability.

### ECMA-262 spec

* 11.9.3 The Abstract Equality Comparison Algorithm: http://www.ecma-international.org/ecma-262/5.1/#sec-11.9.3
* 11.9.6 The Strict Equality Comparison Algorithm: http://www.ecma-international.org/ecma-262/5.1/#sec-11.9.6

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#equality


## Comparing two non-primitive values

You should take special note of the `==` and `===` comparison rules if you're comparing two non-primitive values, like `object`s (including `function` and `array`). Because those values are actually held by reference, both `==` and `===` comparisons will simply check whether the references match, not anything about the underlying values.

For example, `array`s are by default coerced to `string`s by simply joining all the values with commas (`,`) in between. You might think that two `array`s with the same contents would be `==` equal, but they're not:

```js
var a = [1,2,3];
var b = [1,2,3];
var c = "1,2,3";

a == c;  // true
b == c;  // true
a == b;  // false
```

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#equality
