## Notes

A virtual machine enables the same platform to run on multiple operating systems
and hardware architectures. The Interpreters for Java and Python can be taken as
examples, where the code is compiled into their VM specific bytecode. 

What should a virtual machine generally implement? It should emulate the
operations carried out by a physical CPU and thus should ideally encompass the
following concepts:

* Compilation of source language into VM specific bytecode
* Data structures to contains instructions and operands (the data the
  instructions process)
* A call stack for function call operations
* An "Instruction Pointer"" (IP) pointing to the next instruction to execute
* A virtual "CPU" – the instruction dispatcher that
    - Fetches the next instruction (addressed by the instruction pointer)
    - Decodes the operands
    - Executes the instruction

On stack vs. register based VMs: The difference between the two approaches is in
the mechanism used for storing and retrieving operands and their results.

In the register based implementation of a virtual machine, the data structure
where the operands are stored is based on the registers of the CPU. There is no
PUSH or POP operations here, but the instructions need to contain the addresses
(the registers) of the operands. That is, the operands for the instructions are
explicitly addressed in the instruction, unlike the stack based model where we
had a stack pointer to point to the operand. For example, if an addition
operation is to be carried out in a register based virtual machine, the
instruction would more or less be as follows:

```
ADD R1, R2, R3 ;        # Add contents of R1 and R2, store result in R3
```

As I mentioned earlier, there is no POP or PUSH operations, so the instruction
for adding is just one line. But unlike the stack, we need to explicitly mention
the addresses of the operands as R1, R2, and R3. The advantage here is that the
overhead of pushing to and popping from a stack is non-existent, and
instructions in a register based VM execute faster within the instruction
dispatch loop.


## Glossary

* **Bytecode**, also known as p-code (portable code), is a form of instruction
  set designed for efficient execution by a software interpreter. The name
  bytecode stems from instruction sets which have one-byte opcodes followed by
  optional parameters. Bytecode may often be either directly executed on a
  virtual machine (i.e. interpreter), or it may be further compiled into machine
  code for better performance.
* Opcodes can be found in so called byte codes and other representations
  intended for a software interpreter rather than a hardware device. 


## Notes

Having all operands in the instruction has its benefits; the execution is faster
compared to the stack VM, which needs a small calculation to find out the
operand, while register VMs just read the registers.

Also, a stack VM might consume more memory cycles, since it uses a set of
registers to simulate a stack. Besides, temporary values often spill out into
the main memory, adding more memory cache cycles.

In register VMs, temporary values usually remain in registers. Stack VMs are
unable to use a few optimisations too. For example, in the case of common
sub-expressions, which are recalculated each time they appear in the code, a
register VM can calculate an expression once, and keep that in a register for
all future references.


## Reading

* What is stack and heap? http://stackoverflow.com/questions/79923/what-and-where-are-the-stack-and-heap
* http://duartes.org/gustavo/blog/post/anatomy-of-a-program-in-memory
* Memory Management: Overview http://www.memorymanagement.org/articles/begin.html
* http://en.wikipedia.org/wiki/Stack_machine
* http://en.wikipedia.org/wiki/Register_machine
* http://www.incubatorgames.com/index.php/20110621/simple-scripting-language-part-5/
