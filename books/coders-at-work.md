# Coders at Work

## Simon Peyton Jones

* [The Computer Scientist as Toolsmith][toolsmith] by Fred Brooks

[toolsmith]: http://www.cs.unc.edu/~brooks/Toolsmith-CACM.pdf

## Peter Norvig

**Seibel:** And you studied computers in college but didn't major in computer
science, right?

**Norvig:** When I started, the computer classes were part of the applied-math
department. By the time I graduated there actually was a computer science
department, but I stuck with math as my major. **It felt like doing all the
requirements for a computer science major was like majoring in IBM.** You had
to learn their assembly language, you had to learn their 360 operating system,
and so on. *That didn't seem like much fun.* There were some some courses that
I liked and I took those, but I didn't want to go through all the requirements.

After college I worked for two years, for a software company in Cambridge. And
after two years I said, *"It took me four years to get sick of school and only
two years to get sick of work, maybe I like school twice as much."*

## Brendan Eich

**Seibel:** When you read a big piece of code, how do you get into it?

**Eich:** I used to start top-down. If it's big enough you get function
pointers and control flow gets opaque. I sometimes drive it in the debugger
and play around with it that way. Also, I look for bottom-up pattern that I
recognize. If it's a language processor or if it's got something that makes
system calls that I understand, I can start looking at how those primitives
are used. How does that get used by higher levels in the system? And that
helps me get around. But really understanding it is this gestalt process that
involves looking at different angles of top and bottom and different views of
it, playing in the debugger , stepping through in the debugger - incredibly
tedious though that can be.

If you can understand what's going on a little bit in the heap - chase
pointers, walk through cons cells, whatever - that can be worth the trouble
though it gets tedious. That, to me, is as important as reading source. You
can get a long way reading source; you can also get stuck and get bored and
convince yourself you understand something that you don't.

When I did JavaScript's regular expressions I was looking at Perl 4. I did
step through it in the debugger, as well as read the code. And that gave me
ideas; the implementation I did was similar. In this case recursive
backtracking nature of them was a little novel, so that I had to wrap my head
around. It did help to just debug simple regular expressions, just to trace
the execution. I know other programmers talk about this: you should step
through code, you should understand what the dynamic state of the program
looks like in various quick bird's-eye view or sanity checks, and I agree with
that.

## Douglas Crockford

**Seibel:** When you're hiring programmers, how do you recognize the good ones?

**Crockford:** The approach I've taken now is to do a code reading. I invite
the candicate to bring in a piece of code he's really proud of and walk us
through it.

**Seibel:** And what are you looking for?

**Crockford:** I'm looking for quality of presentation. I want to see what he
thinks is something he's proud of. I want to see evidence that in fact he is
the author of the thing that he's defending. *I find that is much more
effective than asking them to solve puzzles or trivia questions. I see all that
kind of stuff as useless.* But how effectively they can communicative, that's
a skill that I'm hiring for.
