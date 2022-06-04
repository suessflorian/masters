# Mutex, Condition Variables, Semiphore, Spinlocks
Lecture reviews lecture 20 content for the first 10min, precisely the difference between "Mutex" and "Condition Variable".

Thinking about:
```csharp
mutex m = new mutex();
condition_variable cv = new 
condition_variable();
bool desiredStateReached = false;
m.lock();
while (!desiredStateReached)
	cv.wait(m); // "waits thread"
m.unlock();
```

Occurring concurrently to:
```csharp
m.lock();
desiredStateReached = true;
cv.signal(); // wakes up "waiting" threads
m.unlock();
```

## Mutex
Used by multiple threads to ensure integrity of a shared object. Allows access to one thread at a time.
**Two states, locked, unlocked**

Each thread when wanting to cross a `critical section` requests to lock the mutex. If thread encountered the mutex in an unlocked state, it proceeds to lock and enter the critical section. If it encounters a locked mutex, it waits. (Effectively being blocked until mutex is unlocked).

Single mutex across many different threads.

It is the lock is unlocked, the thread is put to sleep: the OS saves the entire thread context and pushes it out of the processor core into sleep queue. The processor core becomes available for use by another thread or process.

The thread will transition from a sleep queue to a runnable queue when the OS see's the mutex unlocked. So if a thread is at the top of a runnable queue AND a core is available, the thread context is loaded back to a processor and continued as per intuition suggests.

## Spinlock
Spinlock is a dumber version of a mutex, where rather than offloading from a core when a locked mutex is encountered. We instead _spin_ inside, polling the mutex status until progress can be made. This obviously hogs resources. But sidesteps the whole marshalling and unmarshalling of a thread context.

## Condition Variable
Allows a thread to wait until signalled to "try again". Synchronization tool used in conjunction to a mutex.

# Complex Synchronisation Objects
Supposedly a combination of condition variables and mutex can be used to construct reader-writer locks...

### reader-writer lock
In general, considering some data store as a concrete example, read operations exceed write operations. Reads concurrently can be permitted. But writing cannot. Reading and writing **cannot** be done simultaneously.

A mutex on it's own can only mutually exclude all or no operations. Hence being wasteful when restricting read operations.

> Design and implement (using pseudo-code) a `ReadWriteLock` object that allows concurrent read accesses, but disallows concurrent write or read/write accesses. You may use simple mutexes and/or condition variables in your code. 

_Note: question is important to dwell on, as this is a handheld exam style question_

```go
...
import (
	mutex
	sync
)

...

type ReadWriteLock struct {
	currentReaders int
	m *mutex.Mutex
	cond *sync.Cond
}

func NewReadWriteLock() *ReadWriteLock {
	lock := &ReadWriteLock{
		m: mutex.New(),
	}
	lock.cond = sync.NewCond(lock.m)
	return lock
}

func (r *ReadWriteLock) ReadLock() {
	r.m.Lock()
	defer r.m.Unlock()
	r.currentReaders++
}

func (r *ReadWriteLock) ReadUnlock() {
	r.m.Lock()
	defer r.m.Unlock()
	r.currentReaders--
	r.cond.Signal()
}

func (r *ReadWriteLock) WriteLock() {
	r.m.Lock()
	while !(r.currentReaders == 0) { r.cond.Wait(m) }
}

func (r *ReadWriteLock) WriteUnlock() {
	r.cond.Signal()
	r.m.Unlock()
}
```
