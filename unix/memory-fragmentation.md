Aaron: Sure. So, one of the issues that we had at, well, we have this issue at
GitHub too, is that our heap gets fragmented. We use forking processes, our web
server forks, and eventually it means that all of the memory pages get copied
out at some point. This is due to fragmentation. When you have a fragmented
heap, when we allocate objects, we are allocating into those free slots and so
since we're doing writes into those slots, it will copy those pages to child
processes. So, what would be nice, is if we could eliminate that fragmentation
or reduce the fragmentation and maybe we wouldn't copy the child pages so much.
Doing that, reducing the fragmentation like that, can improve locality but not
necessarily. If it does, if you are able to improve the locality by storing
those objects close to each other in memory, they will be able to hit caches
more easily. If they hit those caches, you get faster access, but you can't
predict that.

Matz: Do you have any proof on this? Or a plan?

Aaron: Any plan? Well yes, I prepared a patch that...

Matz: Making it easier to separate the heap.

Aaron: Yes, two separate heaps. For example with classes or whatever types with
classes, we’ll allocate them into a separate heap, because we know that classes
are probably not going to get garbage collected so we can put those into
a specific location.

[Reference](https://blog.heroku.com/ruby-3-by-3/)
