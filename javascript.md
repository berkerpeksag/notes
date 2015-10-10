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


## `"foo" < "bar"`

JavaScript `string` values can also be compared for inequality, using typical
alphabetic rules (`"bar" < "foo"`).

What about coercion? Similar rules as `==` comparison (though not exactly
identical!) apply to the inequality operators. Notably, there are no "strict
inequality" operators that would disallow coercion the same way `===` "strict
equality" does.

```js
var a = 41;
var b = "42";
var c = "43";

a < b;  // true
b < c;  // true
```

In section [11.8.5](http://www.ecma-international.org/ecma-262/5.1/#sec-11.8.5)
of the ES5 specification, it says that if both values in the `<` comparison are
strings, as it is with `b < c`, the comparison is made lexicographically (aka
alphabetically like a dictionary). But if one or both is not a string, as it is
with `a < b`, then both values are coerced to be numbers, and a typical numeric
comparison occurs.

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#inequality


## Hoisting

Wherever a `var` appears inside a scope, that declaration is taken to belong to
the entire scope and accessible everywhere throughout.

Metaphorically, this behavior is called hoisting, when a var declaration is
conceptually "moved" to the top of its enclosing scope.

```js
var a = 2;

foo();  // works because foo() declaration is "hoisted"

function foo() {
    a = 3;

    console.log( a );  // 3

    var a;  // declaration is "hoisted" to the top of foo()
}

console.log( a );  // 2
```

### Variable declaration vs. assignment

```js
var text = 'outside';

function logIt() {
  console.log(text);
  var text = 'inside';
};

logIt();
```

Variable declarations are "hoisted" to the top of the current scope. Variable
assignments, however, are not.

The declaration (but not the assignment) of text gets hoisted to the top of
`logIt()`. So our code gets interpreted as though it were:

```js
var text = 'outside';

function logIt() {
  var text;
  console.log(text);
  text = 'inside';
};

logIt();
```

**References:**

1. https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#hoisting
2. https://www.interviewcake.com/question/python/js-scope


## `let`

ES6 lets you declare variables to belong to individual blocks (pairs of `{ ..
}`), using the `let` keyword.

```js
function foo() {
    var a = 1;

    if (a >= 1) {
        let b = 2;

        while (b < 5) {
            let c = b * 2;
            b++;
            console.log( a + c );
        }
    }
}

foo();  // 5 7 9
```

Because of using `let` instead of `var`, `b` will belong only to the `if`
statement and thus not to the whole `foo()` function's scope. Similarly, `c`
belongs only to the `while` loop.

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#nested-scopes


## Function definitions

```js
var foo = function() {
    // ..
};

var x = function bar(){
    // ..
};
```

The first function expression assigned to the `foo` variable is called
anonymous because it has no name.

The second function expression is named (`bar`), even as a reference to it is
also assigned to the `x` variable.

Named function expressions are generally more preferable, though anonymous
function expressions are still extremely common.

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#functions-as-values


## Module pattern

The most common usage of closure in JavaScript is the module pattern. Modules
let you define private implementation details (variables, functions) that are
hidden from the outside world, as well as a public API that is accessible from
the outside.

```js
function User() {
    var username, password;

    function doLogin(user,pw) {
        username = user;
        password = pw;

        // do the rest of the login work
    }

    var publicAPI = {
        login: doLogin
    };

    return publicAPI;
}

// create a User module instance
var fred = User();
fred.login("fred", "12Battery34!");
```

The `User()` function serves as an outer scope that holds the variables
`username` and `password`, as well as the inner `doLogin()` function; these are
all private inner details of this `User` module that cannot be accessed from
the outside world.

### `new User()` vs. `User()`

We are not calling `new User()` here because `User()` is just a function, not
a class to be instantiated, so it's just called normally. Using `new` would be
inappropriate and actually waste resources.

Executing `User()` creates an instance of the `User` module -- a whole new
scope is created, and thus a whole new copy of each of these inner
variables/functions.

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#modules


## `this`

If a function has a `this` reference inside it, that `this` reference usually
points to an `object`. But which `object` it points to depends on how the
function was called.

It's important to realize that `this` does not refer to the function itself, as
is the most common misconception.

```js
function foo() {
    console.log( this.bar );
}

var bar = "global";

var obj1 = {
    bar: "obj1",
    foo: foo
};

var obj2 = {
    bar: "obj2"
};

foo();              // "global"
obj1.foo();         // "obj1"
foo.call( obj2 );   // "obj2"
new foo();          // undefined
```

There are four rules for how this gets set, and they're shown in those last
four lines of that snippet.

1. `foo()` ends up setting `this` to the global object in non-strict mode -- in
   strict mode, `this` would be `undefined` and you'd get an error in accessing
   the `bar` property -- so "global" is the value found for `this.bar`.
2. `obj1.foo()` sets `this` to the `obj1` object.
3. `foo.call(obj2)` sets `this` to the `obj2` object.
4. `new foo()` sets `this` to a brand new empty object.

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#this-identifier


## Prototypes

When you reference a property on an object, if that property doesn't exist,
JavaScript will automatically use that object's internal prototype reference to
find another object to look for the property on. You could think of this almost
as a fallback if the property is missing.

```js
var foo = {
    a: 42
};

// create bar and link it to foo
var bar = Object.create(foo);

bar.b = "hello world";

bar.b;  // "hello world"
bar.a;  // 42 <-- delegated to `foo`
```

The `a` property doesn't actually exist on the `bar` object, but because `bar`
is prototype-linked to `foo`, JavaScript automatically falls back to looking
for a on the `foo` object, where it's found.

**Reference:** https://github.com/getify/You-Dont-Know-JS/blob/master/up%20%26%20going/ch2.md#prototypes
