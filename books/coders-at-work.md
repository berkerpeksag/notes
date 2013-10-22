# Coders at Work

## Simon Peyton Jones

### Books or Papers

* [The Computer Scientist as Toolsmith][toolsmith] by Fred Brooks
* Programming Pearls by Jon Bentley
* "Writing Programs for 'The Book'" chapter in Beautiful Code by Brian Hayes
* Purely Functional Data Structures by Chris Okasaki

[toolsmith]: http://www.cs.unc.edu/~brooks/Toolsmith-CACM.pdf

## Joe Armstrong

**Seibel:** Is there anything that you have done specifically to improve your
skill as a programmer?

**Armstrong:** It's a motivating force to implement something; I really
recommend it. If you want to understand C, write a C compiler. If you want to
understand Lisp, write a Lisp compiler or a Lisp interpreter. I've had people
say, *"Oh, wow, it's really difficult writing a compiler."* It's not. It's quite
easy. There are a lof of little things you have to learn about, none of which is
difficult.

* You have to know about data structures.
* You need to know about hash tables.
* You need to know about parsing.
* You need to know about code generation.
* You need to know about interpretation techniques.

Each one of these is not particulary difficult. Things you don't do are
difficult and things you've done are easy. So you don't even try. And I think
that's a mistake.

**Seibel:** What are the techniques that you use for debugging? Print
statements?

**Armstrong:** Print statements. The great gods of programming said, *"Thou
shalt put `printf` statements in your program at the point where you think it's
gone wrong, recompile, and run it."*

Then there's -- I don't know if I read it somewhere or if I invented it myself
-- *Joe's Law of Debugging*, which is that all errors will be plus/minus three
statements of the place you last changed the program.

**Seibel:** Some companies are famous for using logic puzzles during
interviews. Do you ask people that kind of questions in interviews?

**Armstrong:** No. Some very good programmers are kind of slow at that kind of
stuff.

### Quotes

* The really good programmers spend a lot of time programming. I haven't seen
  very good programmers who don't spend a lot of time programming. If I don't
  program for two or three days, I need to do it. And you get better at it --
  you get quicker at it.
* To me programming isn't about typing code into a machine. Programming is about
  understanding.
* There is no point learning lots of languages that all do the same thing.
* I can hardly read or write C++. I don't like C++; it doesn't feel right. It's
  just complicated. I like small simple languages. It didn't feel small and
  simple.
* I like documentation. I don't think a program is finished until you've written
  some reasonable documentation. I think it's unprofessional these people who
  say, *"What does it do? Read the code."* The code shows me what is *does*. It
  doesn't show me what it's supposed to do.
* I should go back to Prolog -- drop Erlang.
* Spend 20 percent of your time learning stuff.
* Ugly is when it's done with a linear search and it could have been done with a
  binary interval halving. Or it could have done logarithmically and it's done
  linearly. For the wrong reasons. Sure do it linearly if we know we're
  searching through a list of ten elements, who cares? But if it's a big data
  structure then it should have been done with a binary search. And so it's
  really not very pretty to do it in a linear form.
* **Seibel:** I heard about a computer science department where in the tutor's
  office they had a stuffed animal and the rule was you had to explain your
  problem to the stuffed animal before you could bother tutor. *"OK,  Mr. Bear,
  here's the thing I'm working on and here's my approach--aha! There it is."*
* Big mistake: don't tell people how fast something is going to be *before*
  you've implemented it.
* ...then I thought I could implement this abstract machine in C so I started
  writing my first-ever C. And Mike Williams came along and looked at my C and
  said, *"This is the worst C I've ever seen in my entire life. This is
  appallingly bad."*

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

**Seibel:** What about *The Art of Computer Programming*? Some of the people
I've talked to on this have absolutely read it from cover to cover. Some people
have it on the shelf and use it as a reference. And some people just have it on
the shelf.

**Norvig:** At one point I had it as *my monitor stand* because it was one of
  the biggest set of books I had, and it was just the right height.

## Brendan Eich

**Seibel:** Let's go back to those ten days when you implemented the original
JavaScript. I know that at some point someone had turned you on to Abelson and
Sussman and your original idea was to put Scheme in the browser.

**Eich:** The immediate concern at Netscape was it must look like Java. People
have done Algol-like syntaxes for Lisp but I didn't have time to take a Scheme
core so I ended up doing it all directly and that meant I could make this same
mistakes that others made.

I didn't have total dynamic scope, like Stallman insisted was somehaw important
for Emacs and infested Elisp with. JavaScript has mostly lexical scope wite some
oddness to it - there are a few loopholes that are pretty much dynamic: the
global object, the `with` statement, `eval`. But it's not like dollar variables
in Perl before `my` or `upvar`, `uplevel` in Tcl. The '90s was full of that --
it was trendy.

But I didn't stick to Scheme ant it was because of the rushing. I had too little
time to actually think through some of the consequences of things I was doing.
I was economizing on the number of objects that I was going to have to
implement in the browser. So I made the global object be the window object,
which is a source of unknown new name bindings and makes it impossible to make
judgments about free variables. So that was regrettable.

**Seibel:** Did you ever consider making a language more closely related to Java
-- take Java and make some kind of simple subset; get rid of the primitive types
and other needless complexities?

**Eich:** There was some pressure from management to make the syntax look like
Java. There was also some pressure to make it not too big, because after all,
people should use Java if they're doing any real programming; this is just
Java's dumb little brother.

**Seibel:** How do you decide when it's right to do a big rewrite? Thanks to
Joel Spolsky, Netscape is in some ways the poster child for the dangers of the
big rewrite.

**Eich:** There was an imperative from Netscape to make the acquisition that
waved the *Design Patterns* book around feel like they were winners by using
their new rendering engine,  which was like *My First Object-Oriented
Rendering Engine*. From a high level it sounded good; it used C++ and design
patterns. But it had a lot of problems.

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

### Quotes

* I'm not really looking for respect, especially from the Java-heads or the
  trailing edge.
* I have this big allergy to ivory-tower design and design patterns. Peter
  Norvig, when he was at Harlequin, he did this paper about how design patterns
  are really just flaws in your programming language. Get a better programming
  language. He's absolutely right. Worshipping patterns and thinking about,
  "Oh, I'll use the X pattern."
* I don't give people puzzles to solve. Google does that in spades, and they
  hire a bunch of very bright puzzle-solvers.


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

**Seibel:** What about Knuth's magnum opus, *The Art of Computer Programming*?
Are you the kind of person who read it cover to cover, who dips into it for
reference, or who put it on the shelf and never looked at it?

**Crockford:** All except the last one. When I was in college, there were a
couple of months where I didn't pay rent in order to buy copies of his books.
And I read them and found jokes in them, like there's a TUG joke in the index
of Volume I. I have not been able to make sense out of all of it. There are
places where he goes really a lot deeper than I can go, but I enjoy the books
a lot, and I've also used them as reference books.

**Seibel:** Did you literally read them cover to cover, skimming over the math
that you couldn't understand?

**Crockford:** Yeah, the part when there are too many stars, I would read it
very quickly. I tried to make familiartiy with Knuth a hiring criteria, and
I was disappointed that I couldn't find enough people that had read him. *In my
view, anybody who calls himself a professional programmer should have read
Knuth's book or at least should have copies of his books.*

**Seibel:** To read Knuth, it seems to me, you have to be able to read the math
and understand it. To what extent do you think having that kind of mathematical
training is necessarily to be a programmer?

**Crockford:** Obviously it's not, because most of them don't have it. In the
sorts of applications that I'm working on, we don't see that much application
of the particular tools that Knuth gives us. If we were writing operating
systems or writing runtimes, it'd be much more critical. But we're doing form
validations and UIs. Generally performance is not that important in the things
that we do. We spend most of our time waiting for the user or waiting for the
network.

I would like to insist that it's absolutely necessary for people to understand
this stuff, but it's not. And maybe that's why web programming has taken off
and why it's so accessible and why JavaScript works. This stuff really isn't
that hard. And most of the things that make it hard are unnecessarily hard. If
we just cleaned up the platform a little bit, this work gets a lot easier.

### Quotes

* I think an hour of code reading is worth two weeks of QA.


## L. Peter Deutsch

### Quotes

* Smalltalk is somewhat better than Simula-67. But Smalltalk as it exists today
  essentially existed in 1976. I'm not saying that today's languages aren't
  better than the languages that existed 30 years ago. The language that I do
  all of my programming in today, Python, is, I think, a lot better than
  anything that was available 30 years ago. I like it better than Smalltalk.
* Every now and then I feel a temptation to design a programming language but
  then I just lie down until it goes away.
* Gosh,  here we have Smalltalk, which has this really great code-generation
  machinery, which is now very mature - it's about 20 years old and it's
  extremely reliable. It's a relatively simple, relatively retargetable,
  quite efficent just-in-time code generator that's designed to work really
  well with non type-declared languages. On the other hand, here's Python,
  which is this wonderful language with these wonderful libraries and a
  slow-as-mud implementation. Wouldn't it be nice if we could bring the two
  together?
* The difference is that the principles for dealing with algorithmic
  problems are based a lot more directly on 5,000 or 10,000 years' worth of
  history in mathematics. How we go about programming now, we don't have
  anything like that foundation to build on. Which is one of the reasons why so
  much software is crap: we don't really now what we're doing yet.
* Software is a discipline of detail, and that is a deep, horrendous fundamental
  problem with software. Until we understand how to conceptualize and organize
  software in a way that we don't have to think about how every little piece
  interacts with every other piece, things are not going to get a whole lot
  better. And we're very far from being there.
* I'm not really much of an optimist about the future of computing. To be
  perfectly honest, that's one of the reasons why it wasn't hard for me get out.
  I mean, I saw a world that was completely dominated by an unethical monopolist,
  and I didn't see much of a place for me in it.
