* epoll and poll are better than select because the Python program does not
  have to inspect each socket for events of interest. Instead it can rely on
  the operating system to tell it which sockets may have these events.
* epoll is better than poll because it does not require the operating system to
  inspect all sockets for events of interest each time it is queried by the
  Python program. Rather Linux tracks these events as they occur, and returns
  a list when queried by Python.
* epoll has two modes of operation, called edge-triggered and level-triggered.
* In the edge-triggered mode of operation a call to epoll.poll() will return an
  event on a socket only once after the read or write event occurred on that
  socket. The calling program must process all of the data associated with that
  event without further notifications on subsequent calls to epoll.poll(). When
  the data from a particular event is exhausted, additional attempts to operate
  on the socket will cause an exception.
* Conversely, in the level-triggered mode of operation, repeated calls to
  epoll.poll() will result in repeated notifications of the event of interest,
  until all data associated with that event has been processed. No exceptions
  normally occur in level-triggered mode.
* Since they're similar, level-triggered mode is often used when porting an
  application that was using the select or poll mechanisms, while
  edge-triggered mode may be used when the programmer doesn't need or want as
  much assistance from the operating system in managing event state.
* In addition to these two modes of operation, sockets may also be registered
  with the epoll object using the EPOLLONESHOT event mask. When this option is
  used, the registered event is only valid for one call to epoll.poll(), after
  which time it is automatically removed from the list of registered sockets
  being monitored.

**Resources:**

* http://scotdoyle.com/python-epoll-howto.html
* http://lse.sourceforge.net/epoll/index.html
