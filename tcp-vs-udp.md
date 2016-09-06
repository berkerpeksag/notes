# TCP vs. UDP

### TCP

* Connection based
* Guaranteed reliable and ordered
* Automatically breaks up your data into packets for you
* Makes sure it doesn’t send data too fast for the internet connection to
  handle (flow control)
* Easy to use, you just read and write data like its a file


### UDP

* No concept of connection, you have to code this yourself
* No guarantee of reliability or ordering of packets, they may arrive out of
  order, be duplicated, or not arrive at all!
* You have to manually break your data up into packets and send them
* You have to make sure you don’t send data too fast for your internet
  connection to handle
* If a packet is lost, you need to devise some way to detect this, and resend
  that data if necessary


### Notes

* You should never use TCP for networking time-critical data.
* We want our data to get as quickly as possible from client to server without
  having to wait for lost data to be resent.
* TCP and UDP are both built on top of IP, but they are radically different.
  UDP behaves very much like the IP protocol underneath it, while TCP abstracts
  everything so it looks like you are reading and writing to a file, hiding all
  complexities of packets and unreliability from you.
* TCP is a stream protocol, so you just write bytes to a stream, and TCP makes
  sure that they get across to the other side. Since IP is built on packets,
  and TCP is built on top of IP, TCP must therefore break your stream of data
  up into packets. So, some internal TCP code queues up the data you send, then
  when enough data is pending the queue, it sends a packet to the other
  machine. [1]
* It all stems from how TCP handles lost and out of order packets, to present
  you with the "illusion" of a reliable, ordered stream of data. Fundamentally
  TCP breaks down a stream of data into packets, sends these packets over
  unreliable IP, then takes the packets received on the other side and
  reconstructs the stream. [2]

---

**Footnotes:**

1. This can be a problem for multiplayer games if you are sending very small
   packets. What can happen here is that TCP may decide that its not going to
   send data until you have buffered up enough data to make a reasonably sized
   packet (say more than 100 bytes or so).

   TCP has an option you can set that fixes this behavior called `TCP_NODELAY`.
   This option instructs TCP not to wait around until enough data is queued up,
   but to send whatever data you write to it immediately. This is typically
   referred to as disabling Nagle’s algorithm.
2. In essence TCP sends out a packet, waits a while until it detects that
   packet was lost because it didn’t receive an ack (acknowledgement) for it,
   then resends the lost packet to the other machine. Duplicate packets are
   discarded on the receiver side, and out of order packets are resequenced so
   everything is reliable and in order.

**Reference:** http://gafferongames.com/networking-for-game-programmers/udp-vs-tcp/
