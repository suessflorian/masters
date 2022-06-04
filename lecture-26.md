# MIPS Processor Design
RISC (reduced instruction set computer).

## Instruction Set Architecture (ISA)
- Assembler; translates assembly to machine language.
- Compilers; high-level language to assembly.

ISA mostly uses assembly language to denote machine capabilities.

# Storage Space
Process has two sets of storage space, **registers** and **linear array** memory.

Memory is organised as bytes (8 bits), each byte is individually addressable. 

- A **word** is the smallest unit of data that we can get in/out of mem.

Word is typically either 4 bytes (32bit) or 8 bytes (64bit). In MIPS, it'll be 4 bytes. So in a `2^32` byte system with byte address `0-2^32-1`, we'd have `2^30` words with byte addresses 0, 4, 8, ..., `2^32-4`. (Divid bytes by 4, offset addresses for to every 4th...)

For Registers, MIPS has 32, each holding a word (4 bytes, 32 bits).

There are a bunch of registers reserved. See slides. Notable mentions.

The zero register, spots for evaluating function expressions. OS Kernel. Global pointer, stack pointer, frame pointer, return address.

# Some MIPS instructions
- `add $s1, $s2, $s3` => `$s1 = $s2 + $3` (instruction type R)
- `bne $s4, $s5, Label` => if `$s4 != $s5` goto Label (instruction type I)
- `lw $s1, 100($s2)` => load word `$s1 = Memory[100 + $s2]`
- `sw $s1, 100($s2)` => store word `Memory[100+$s2] = $s1`
- `j Label` => jump to Label (instruction type J)

# Instruction Types
R, 6bits to denote OPERATION, 5bits each ARG, ARG, ARG, SHAMT(?), 6bits FUNC(?)
I, 6bits to denote OPERATION, 5bits each ARG, ARG, 16bits label address
J, 6bits to denote OPERATION, 26bit label address

- _Note addresses given here are offsets from current program counter (PC)_

Notice how the `J` type instruction can pounce you a lot further than `I` type instructions.

Question: how can we do a longer branch than permissable by `I`?

```
					bneq $s4, $s5, nearby
					j faraway label
nearby    ...
...
...
faraway   ...
```

# Assembler Macros
Just like macro's in Rust. These are convience instructions that can be used to compact the overall assembly described in a program

Eg: move $t0, $t1 can be defined as add $t0, $t1, $zero

---

Question: MIPS has an slt (set if less than) instruction: `slt $t1, $s1, $s2` will set `$t1` to one if `$s1` is less than `$s2`, otherwise it clear `$t1` (i.e., set it to 0). How would you implement a new blt (`branch less than`) instruction as an assembler macro using slt and bne?

Answer:

```
slt $t1, $s1, $s2
bne $t1, $zero, label
```

# Interjection
There's a ton of different things you can do, you could classify them as
- Arithmetic (add, multiply, immediate add)
- Logical (and, or)
- Data Transfer (store/load word)
- Control Flow (branch if equal, inequaltiy based setting, jumps)

# Example Converting High-Level to MIPS Assembly

suppose
```javascript
// there's some array
for (let i=0; i<10; ++i) {
	sum += array[i];
}
```

Assuming the array has pointer elements, each pointer being 4 bytes long, lets assume `$a0` is currently pointing to the 0th element. Then `$addiu $a0 4` is pointing to the next element and so on.

To de-reference the 0th element you'd have to `$lw $e0 0($a0)`, 1th element would be `$lw $e1 4($a0)`... and so on.

```
			add $iteration $zero $zero
			addiu $upper $zero 10
			add $sum $zero $zero

LOOP: beq $iteration $upper EXIT
			add $pointer $iteration
			
			addiu $iteration 1
			j LOOP

EXIT: ...
```

I abandoned the above... because I'm spending too much time.

This following was formulated in the slides;

`$a0` marks points to the start of the array. `$t9` points to the memory address of the 9th element of the array (each element in the array is a word, 4 bytes long).

`$s0` will denote the sum. We loop through incrementing the `$a0` in jumps of 4.

```
				addiu $t9, $a0, 40
	Loop: beq $a0, $t9, Exit
				lw $t0, 0($a0)
				add $s0, $s0, $t0
				addiu $a0, $a0, 4
				j Loop
	Exit: ...
```

## Speeding Up Loops

We can turn this;
```
				addiu $t9, $a0, 40
	Loop: beq $a0, $t9, Exit
				lw $t0, 0($a0)
				add $s0, $s0, $t0
				addiu $a0, $a0, 4
				j Loop
	Exit: ...
```

Into this;
```
				addiu $t9, $a0, 40
				beq $a0, $t9, Exit
	Loop: lw $t0, 0($a0)
				add $s0, $s0, $t0
				addiu $a0, $a0, 4
				bne $a0, $t9, Loop
	Exit: ...
```

And we can employ loop unrolling to take those 4 instructions per loop above and turn it into

```javascript
let sum = 0;
for (let i = 0;	i < 10; i+=1) { 
	sum += array[i];
	++i;
	sum += array[i];
}
```

```
				addiu $t9, $a0, 40
				beq $a0, $t9, Exit
	Loop: lw $t0, 0($a0)
				add $s0, $s0, $t0
				addiu $a0, $a0, 4
				lw $t0, 0($a0)
				add $s0, $s0, $t0
				addiu $a0, $a0, 4
				bne $a0, $t9, Loop
	Exit: ...
```

Which processes 7 instructions per 2 iterations, although this requires the iterations nessecary to be divisble by this "unrolling factor"

Can optimise further by making use of the lw immediate offset... and in each iteration here increment the pointer to elements by 8. This yields a narrower 6 operations per 2 iterations.

```
				addiu $t9, $a0, 40
				beq $a0, $t9, Exit
	Loop: lw $t0, 0($a0)
				add $s0, $s0, $t0

				lw $t0, 4($a0)
				add $s0, $s0, $t0
				addiu $a0, $a0, 8
				bne $a0, $t9, Loop
	Exit: ...
```
