## How do programs call functions in libraries?

Shared libraries can be loaded at any address. This means that functions within
shared libraries will exist at an address that is not known until the library
is loaded at runtime. Subsequent runs of the same program with the same
libraries will load the same libraries at different addresses.

Programs on Linux use the ELF binary format which provides for many features.
For the purposes of understanding how library functions are called, we’ll
direct our attention to the Procedure Linkage Table (PLT) and the Global Offset
Table (GOT).

The PLT contains a group of assembly instructions per library function that
executes when a library function is called. Groups of assembly instructions are
often called “trampolines.”

Here’s an example of a PLT trampoline:

```asm
PLT1: jmp *name1@GOTPCREL(%rip)
      pushq $index1
      jmp .PLT0
```

All of the entries in the PLT follow the same template.

This code starts by jumping to the address stored in an entry in the GOT.

The GOT contains a list of absolute addresses. At program start, these
addresses are initialized to point to the pushq instruction inside the PLT (the
second line in the assembly code above).

The pushq code executes to store some data for the dynamic linker and the jmp
on line 3 runs which transfers execution to another piece of code that calls
into the dynamic linker.

The dynamic linker then uses the value $index1 and other data to find out which
library function the program tried to call. It locates the address of the
library function and writes it to the entry in the GOT overwriting the previous
entry which pointed inside of the PLT.

Any call to the same library function after this point will execute the
function directly instead of invoking the dynamic linker.

To review, the high level summary is:

When the program is loaded into memory the program and each dynamic shared
object (DSO for short, also known as shared library) has their PLT and GOT
mapped into memory.

At the start of execution, the memory locations of functions in a shared
library are not known. This is because a shared library can be loaded at any
address in the address space of a program.

When a library function is called, execution is transferred to the function’s
PLT entry. The PLT entry is a set of assembly instrucions (called
a ‘trampoline’).

This ‘trampoline’ arranges data about the function the program was trying to
call and invokes the dynamic linker.

The dynamic linker runs, takes the data arranged by the PLT trampoline and uses
it to find the address of the function that the program is trying to call.

Once found, the address is written to the GOT and execution is transferred to
the function.

Subsequent calls to the same function do not invoke the dynamic linker.
Instead, the PLT calls directly to the function using the address stored in the
GOT.

[Source](https://blog.packagecloud.io/eng/2016/03/14/how-does-ltrace-work/)
