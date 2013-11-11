# Garbage Collectors

GC systems do much more than just “collect garbage.” In fact, they perform three
important tasks. They

* allocate memory for new objects,
* identify garbage objects, and
* reclaim memory from garbage objects.

Imagine if your application was a human body: All of the elegant code you write,
your business logic, your algorithms, would be the brain or the intelligence
inside the application. Following this analogy, what part of the body do you
think the garbage collector would be?

I think the garbage collector is the beating heart of your application. Just as
your heart provides blood and nutrients to the rest of the your body, the
garbage collector provides memory and objects for your application to use. If
your heart stopped beating you would die in seconds. If the garbage collector
stopped or ran slowly – if it had clogged arteries – your application would slow
down and eventually die!


## A Simple Example

```py
class Node:

    def __init__(self, val):
        self.value = val

print(Node(1))
print(Node(2))
```


## Allocating Objects in Python

While Python also uses free lists for various reasons internally (it recycles
certain objects such as lists), it normally allocates memory for new objects and
values differently than Ruby does.

Python will ask the operating system for memory immediately when you create the
object. (Python actually implements its own memory allocation system which
provides an additional layer of abstraction on top of the OS heap. But I don’t
have time to get into those details today.)

When we create a second object, Python will again ask the OS for more memory.

Seems simple enough; at the moment we create an object Python takes the time to
find and allocate memory for us.

Internally, whenever we create an object Python saves an integer inside the
object’s C structure, called the *reference count*. Initially, Python sets this
value to 1.

The value of 1 indicates there is one pointer or reference to each of the three
objects.

Whenever an object’s reference count reaches zero, Python immediately frees it,
returning it’s memory to the operating system.

This garbage collection algorithm is known as reference counting. It was
invented by George Collins in 1960 – not coincidentally the same year John
McCarthy invented the free list algorithm.

Along with reference counting Python employs a second algorithm called
generational garbage collection. This means Python’s garbage collector handles
newly created objects differently than older ones.


## Cyclic Data Structures and Reference Counting in Python

Python uses an integer value saved inside of each object, known as the reference
count, to keep track of how many pointers reference that object. Whenever a
variable or other object in your program starts to refer to an object, Python
increments this counter; when your program stops using an object, Python
decrements the counter. Once the reference count becomes zero, Python frees the
object and reclaims its memory.

Since the 1960s, computer scientists have been aware of a theoretical problem
with this algorithm: if one of your data structures refers to itself, if it is a
cyclic data structure, some of the reference counts will never become zero.


```py
class Node:

    def __init__(self, val):
        self.value = val

n1 = Node(1)
n2 = Node(2)

n1.next = n2
n2.prev = n1
```

Now let’s suppose our Python program stops using the nodes; we set both `n1` and
`n2` to `None`.

Now Python, as usual, decrements the reference count inside of each node down to
1.


## Generation Zero in Python

We have an “island” or a group of unused objects that refer to each other, but
which have no external references. In other words, our program is no longer
using either node object, therefore we expect Python’s garbage collector to be
smart enough to free both objects and reclaim their memory for other
purposes. But this doesn’t happen because both reference counts are one and not
zero. Python’s reference counting algorithm can’t handle objects that refer to
each other!

Of course, this is a contrived example, but your own programs might contain
circular references like this in subtle ways that you may not be aware of. In
fact, as your Python program runs over time it will build up a certain amount of
“floating garbage,” unused objects that the Python collector is unable to
process because the reference counts never reach zero.

This is where Python’s generational algorithm comes in! Just as Ruby keeps track
of unused, free objects using a linked list (the free list), Python uses a
different linked list to keep track of active objects. Instead of calling this
the “active list,” Python’s internal C code refers to it as Generation
Zero. Each time you create an object or some other value in your program, Python
adds it to the Generation Zero linked list.


## Detecting Cyclic References

Later Python loops through the objects in the Generation Zero list and checks
which other objects each object in the list refers to, decrementing reference
counts as it goes. In this way, Python accounts for internal references from one
object to another that prevented Python from freeing the objects earlier.

Python also uses two other lists called Generation One and Generation Two.

By identifying internal references, Python is able to reduce the reference count
of many of the Generation Zero objects. Above in the top row you can see that
ABC and DEF now have a reference count of zero. This means the collector will
free them and reclaim their memory. The remaining live objects are then moved to
a new linked list: Generation One.

In a way, Python’s GC algorithm resembles the mark and sweep algorithm Ruby
uses. Periodically it traces references from one object to another to determine
which objects remain live, active objects our program is still using – just like
Ruby’s marking process.


## Garbage Collection Thresholds in Python

When does Python perform this marking process? As your Python program runs, the
interpreter keeps track of how many new objects it allocates, and how many
objects it frees because of zero reference counts. Theoretically, these two
values should remain the same: every new object your program creates should
eventually be freed.

Of course, this isn’t the case. Because of circular references, and because your
program uses some objects longer than others, the difference between the
allocation count and the release count slowly grows. Once this delta value
reaches a certain threshold, Python’s collector is triggered and processes the
Generation Zero list using the subtract algorithm above, releasing the “floating
garbage” and moving the surviving objects to Generation One.

Over time, objects that your Python program continues to use for a long time are
migrated from the Generation Zero list to Generation One. Python processes the
objects on the Generation One list in a similar way, after the
allocation-release count delta value reaches an even higher threshold
value. Python moves the remaining, active objects over to the Generation Two
list.

In this way, the objects that your Python program uses for long periods of time,
that your code keeps active references to, move from Generation Zero to One to
Two. Using different threshold values, Python processes these objects at
different intervals. Python processes objects in Generation Zero most
frequently, Generation One less frequently, and Generation Two even less often.


## The Weak Generational Hypothesis

This behavior is the crux of the generational garbage collection algorithm: the
collector processes new objects more frequently than old objects. A new, or
young object is one that your program has just created, while an old or mature
object is one that has remained active for some period of time. Python promotes
an object when it moves it from Generation Zero to One, or from One to Two.

Why do this? The fundamental idea behind this algorithm is known as the weak
generational hypothesis. The hypothesis actually consists of two ideas: that
most new objects die young, while older objects are likely to remain active for
a long time.

Suppose I create a new object using Python:

```py
n1 = Node('ABC')
```

According to the hypothesis, my code is likely to use the new ABC node only for
a short time. The object is probably just an intermediate value used inside of
one method and will become garbage as soon as the method returns. Most new
objects will become garbage quickly in this way. Occasionally, however, my
program creates a few objects that remain important for a longer time – such as
session variables or configuration values in a web application.

By processing the new objects in Generation Zero more frequently, Python’s
garbage collector spends most of its time where it will benefit the most: it
processes the new objects which will quickly and frequently become garbage. Only
rarely, when the allocation threshold value increases, does Python’s collector
process the older objects.


## Mark and Sweep vs. Reference Counting

At first glance, Python’s GC algorithm seems far superior to Ruby’s: why live in
a messy house when you can live in a tidy one? Why does Ruby force your
application to stop running periodically each time it cleans up, instead of
using Python’s algorithm?

Reference counting isn’t as simple as it seems at first glance, however. There
are a number of reasons why many languages don’t use a reference counting GC
algorithm like Python does:

First, it’s difficult to implement. Python has to leave room inside of each
object to hold the reference count. There’s a minor space penalty for this. But
worse, a simple operation such a changing a variable or reference becomes a more
complex operation since Python needs to increment one counter, decrement
another, and possibly free the object.

Second, it can be slower. Although Python performs GC work smoothly as your
application runs (cleaning dirty dishes as soon as you put them in the sink),
this isn’t necessarily faster. Python is constantly updating the reference count
values. And when you stop using a large data structure, such as a list
containing many elements, Python might have to free many objects all at
once. Decrementing reference counts can be a complex, recursive process.

Finally, it doesn’t always work. As we’ll see in my next post containing my
notes from the rest of this presentation, reference counting can’t handle cyclic
data structures – data structures that contain circular references.

At first glance, Ruby and Python seem to implement garbage collection very
differently. Ruby uses John McCarthy’s original mark and sweep algorithm, while
Python uses reference counting. But when we look more closely, we see that
Python uses bits of the mark and sweep idea to handle cyclic references, and
that both Ruby and Python use generational garbage collection in similar
ways. Python uses three separate generations, while Ruby 2.1 uses two.


#### References

* http://patshaughnessy.net/2013/10/24/visualizing-garbage-collection-in-ruby-and-python
* http://patshaughnessy.net/2013/10/30/generational-gc-in-python-and-ruby
