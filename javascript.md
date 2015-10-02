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
