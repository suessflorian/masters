# Pipelining
Provides an efficient way of executing multiple tasks concurrently. We've covered this term before right at the beginning of Mano's section. Laundry example. Looks like we're about to pipeline this multi cycle MIPS datapath. Oof. 

## Load Instruction Recap
- fetches instruction from IM
- register fetch, instruction decode
- address computation via ALU
- memory access
- memory read completion (writing result to register file)

Contrasted against a MIPS diagram.

Then you can contrast the three processor designs, assuming a single datapath we looked at **single** cycle processors, multi cycle processors and now pipelined multi cycle processors.

CPI, average cycle per instruction...

In the lecture we compared the time taken for 100 instructions, CPI ~3.8, single cycle 45ns/cycle, multi-cycle 10ns/cycle.

- single = 45ns/cycle * 1*cycle/instruction * 100 instructions = 4500ns
- multi = 10ns/cycle * 3.8cycles/instruction * 100 instructions = 3800ns
- ideal pipelined = 10ns/cycle * (1 cycle / instruction * 100 instructions + 4 cycles) = 1040ns

# Pipeline Hazards
A hazard prohibits the execution of a planned instruction in the proper cycle. Three forms of hazards may exist in a pipeline.
- structural
- data
- control

## Structural Hazard
When attempting to use the same resource at the same time. Analogy; "combined dryer/washer" then we cannot dry and wash simultaneously.

- occurs when a planned instruction cannot execute in the proper clock cyle because the hardware cannot support the combination of instructions that are set to execute in the given clock cycle.
eg; reading instruction from memory simulatenously to another instruction that is also reading from memory. If you can't have a single logical unit serve both at the same time right...

### Solution
- use separate instruction and data memories rather than a unified one
- have multi-port memory (several concurrent read/write accesses)
- stall the pipeline and wait until the current access completes

## Data Hazard
Arise when attempting to use data that isn't yet ready...
- occur when a planned instruction cannot execute in the proper clock cycle because the data needed to execute the instruction is not available yet.

### Solution
Forwarding the results of dependant instructions ALU outputs to the ALU's of child instructions.
