# Threads & Processes
Each process has it needs it's own set of resources...
- registers
- memory
	- static
	- dynamic
	- code
	- stack

`Fork` is when processes split into two.

Indeed we are entering an era where most processes are multi core, in the sense that they have physical boundaries of the above collection of resources, however we need a lighter version of this process - Where a core can host artificially multiple processes.

## Threads

Threads need their own registers and stack respectively, but they can share all other resources associated to memory (static, dynamic, code etc...).

### Shared Resources
- Address space, shared storage
- The process ID, parent process ID, process group ID
- User ids: real and effective.
- Group ids: real and effective.
- Supplementary group ids
- Current working directory, root directory
- File-mode creation mask
- File descriptor table
- Signal handlers
- Timers

### Private Resources
- Unique thread identifier
- Resources required to support a flow of control (stack)
- C/Unix `errno`
- Thread-specific key/value bindings
- Per-thread cancellation handlers
- Per-thread signal masks
