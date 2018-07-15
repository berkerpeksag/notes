# Code Complete 2

## Quotes

### Chapter 32: Self Documenting Code

> Don't document bad code - rewrite it.

**The Elements of Programming Style** by Kernighan & Plauger (1978)

## Notes

### Chapter 33.3 Curiosity

The worst code I've ever seen was written by someone who wouldn't let anyone go
near her programs. Finally, her manager threatened to fire her if she didn't
cooperate. Her code was uncommented and littered with variables like `x`, `xx`,
`xxx`, `xx1`, and, `xx2`, all of which were global. Her manager's boss thought
she was a great programmer because she fixed errors quickly. The quality of her
code gave her abundant opportunities to demonstrate her error-correcting
ability.

It's no sin to be a beginner or an intermediate. It's no sin to be a competent
programmer instead of a leader. The sin is in how long you remain a beginner or
intermediate after you know what you have to do to improve.

### Chapter 33.4 Intellectual Honesty

> We found that technical people, in general, were actually very good at
> estimating project requirements and schedules. The problem they had was
> defending their decisions; they needed to learn how to hold their ground.

Bill Weimer, IBM (Weimer in Metzger and Boddie 1996)

### Chapter 32.5 Commenting Techniques

**Avoid self-indulgent comments** &#8212; Many years ago, I heard the story of a
maintenance programmer who was called out of bed to fix a malfunctioning
program. The program's author had left the compant and couldn't be reached. The
maintenance programmer hadn't worked on the program before, and after examining
the documentation carefully, he found only one comment. It looked like this:

```asm
MOV AX, 723h	; R. I. P. L. V. B.
```

After working with the program through the night and puzzling over the comment,
the programmer made a succesful patch and went home to bed. Months later, he met
the program's author at a conference and found out that the comment stood for
**"Rest in peace, Ludwig van Beethoven."** Beethoven died in 1827 (decimal),
which is 723 (hexadecimal). The fact that `723h` was needed in that spot had
nothing to do with the comment. Aaarrrghhhhh!

## Articles

* **Programming Considered as a Human Activity** by Edsger Dijkstra, 1965
