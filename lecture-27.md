# Hardware Bits
Must look at lecture slides to get a good idea of all the different diagrams related to circuits.

Looking at various hardware components. Example the **single bit adder**. Output is a carry or not.

Then the **single bit ALU**... You stitch these together to build a **multi bit ALU**.

---
Brief overview given of:
- **combinatorial logic** is a logic circuit whose output depends only on its current input. In contrast,
- in a **sequential logic** circuit, the output will depend on the current input and also some past inputs. *sequential logic circuits have memory*.
---

## Register
A register is s sequential logic circuit. The content of a register can be read anytime, but the register can only be written at the clock's tick only and when `WriteEnable` is set.

## Register File
A set of registers, MIPS has 32 registers in the register file. Has 6 inputs.
`WriteEnable`, `RW`, `RA`, `RB`, `busW`, `Clk`. Outputs `busA` and `busB`.

## Memory
Inputs `WriteEnable`, `Address`, `Clk`, `DataIn`. Outputs `DataOut`. Combinatorial. `DataOut` comes valid after access time. Access time is an instrument to safe guard against logic gate latencies.

## Instruction Fetch Unit
Fetch the instruction; `InstructionMemory[PC]`...
	Update PC; PC = PC + 4.

_We look at a single cucle datapath - arithmetic/logic_

- control signals... Each instruction get's broken up depending on the instruction type.

We just looked at a semi-complete diagram outlining the circuitry of a processor. It's quite rushed overall, this entire segment that is. We will need to just accept that we won't fully understand everything that's here. That's fine.

# Overall Five Steps
1. Fetch instruction
2. Register fetch and instruction decode into control signals
3. ALU execution OR memory address calculation (also using ALU)
4. Read the data from the data memory
5. Write data back to the register file

Some instructions don't need all steps here. The excercise following is a little ridiculous.

# Multiple Cycle Datapath
Some operations would take longer overall than other operations, example of a load
- instruction memory access time
- register file accesst time
- ALU delay (address calculation)
- data memory access time
- register file setup time

So what we do is break each instruction in a series of steps corresponding to the functional unit operations required (ie how many clock cycles an instruction needs).

Means we don't have to slow clock cycles to accomodate the slowest instructions overall time needed.

1. instruction fetch
2. register fetch & instruction decode
3. execution
4. memory access
5. memory read completion

Different instruction types then have different amounts of functional units of operation to perform.

## R-Type
Eg; `R[rd] <- R[rs] + R[rt]; PC <- PC + 4`

- `IR <- MEM[PC]; PC <- PC + 4`... instruction fetch
- `A<-R[rs]; B <-R[rt]`... instruction decode, register fetch
- `ALUOut<-A+B`... execution
- `R[dt] <- ALUOut`... R-Type complete

## Load
Eg; `R[rt] <- Mem[ R[rs] + SignExt(Imm16) ]; PC <- PC + 4`

- `IR <- MEM[PC]; PC <- PC + 4`... instruction fetch
- `A <- R[rs]`... instruction decode, register fetch
- `ALUOut <- A + SignExt(Imm16)`... address computation
- `MDR <-Mem[ALUOut]`... memory access
- `R[rt] <- MDR`... memory read completion

## Store
Eg; `Mem[R[rs] + SignExt(Imm16)] <- R[rt]; PC <- PC + 4`

- `IR <- MEM[PC]; PC <- PC + 4`... instruction fetch
- `A<-R[rs];A<-[rt]`... instruction decode, register fetch
- `ALUOut <- A + SignExt(Imm16)`... address computation
- `Mem[ALUOut] <- B`... memory acccess

## BEQ
EG; `PC <- (R[rs]==R[rt]) ? (PC + 4 + SignExt(Imm16)x4) : (PC + 4)`

- `IR <- MEM[PC]; PC <- PC + 4`... instruction fetch
- `A <- R[rs]; B <- R[rt]; ALUout <- PC + SignExt(Imm16)x4`... instruction decode, register fetch
- `If (A==B) PC <- ALUOut`

Now it's up to use to contrast single cycle datapath and multi cycle datapaths.
