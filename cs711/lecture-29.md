# Continuing on Pipelining Hazards

### Load-use Hazards

```
lw $s0, 20($t1)
sub $t2, $s0, $t3
```

A load-use data hazard can't be solved with fowarding: Must delay/stall instruction dependent on loads. "Delayed" load.

_Note all of these hazards will just need familiarity to get grips with. Hard to learn once over._

With Load word instructions you can still feed a dependent ALU with the output of the DM step, rather than waiting for the load complete step (writing to register file).

## Read-After-Write Data Hazard
RAW hazard can be avoided by forwarding. Looks to be solved in a similar way as a typical Data Hazard?? Forwarding ALU outputs to subsequent instruction ALU stages.

Example;
```
sub $t2, $s0, $t3
add $s0, $t0, $t1
```

## Write-After-Read Data Hazard
Apparently cannot happen? MIPS has 5 stage pipeline, all instructions take 5 stages, reads are always in stage 2, writes are always in stage 5.

## Write-After-Write Data Hazard
Apparently cannot happen? MIPS has 5 stage pipeline, all instructions take 5 stages, reads are always in stage 5.

## Control Hazards
Arise when attempting to make a decision before the condition is evaluated, AKA branch hazard.

```
add $s0, $t0, $t1
beq $t2, $t3, Label
or $s3, $s4, $s5 // do we start evaluting this normally? May or may not happen...
```

> Control hazard occurs when a planned instruction cannot execute in the proper clock cycle because the instruction that is fetched may one be that one that is needed; that is, the flow of instruction addresses is not what the pipeline expected.
