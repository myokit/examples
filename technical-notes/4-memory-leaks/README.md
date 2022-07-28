# Detecting memory leaks in simulations

Goal: Detect memory leaks in myokit simulations (C-extensions compiled on-the-fly).

## Tools:

- [psutil](https://psutil.readthedocs.io)
- [resource](https://docs.python.org/3/library/resource.html)
- [gc](https://docs.python.org/3/library/gc.html)
- tracemalloc
- [pympler](https://pympler.readthedocs.io/en/latest/library/tracker.html) is a great tool that tracks Python objects and the memory they use.

Summary:

Using `psutil` and `resource` we can see the total process memory usage (with some caveats), but we can't learn which parts of our program are using the memory.
Some oddities in the output returned by `psutil` and `resource` are explained by looking at garbage collection via `gc`.
Using `pympler` and `tracemalloc` we can get very detailed insight into memory usage, but only for Python objects (either in pure Python or C extenions, but not memory allocated in C).
Since neither tool is perfect we need both.

### psutil

On linux, we can look at memory usage of a running process with `ps`.

For example, run this:
```
import os
print(f'PID: {os.getpid()}')
input()
```
Then use `ps` from another window to check.
For example, if our PID is 181595:
```
[michael@localhost ~]$ ps u 181111
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
michael   181595  0.1  0.0 229204  8772 pts/2    S+   15:13   0:00 python3 ./test.py
```
The important numbers here are `VSZ` (Virtual memory size) and `RSS` (resident set size).

- [Virtual memory size](https://en.wikipedia.org/wiki/Virtual_memory) shows the total memory allocated to a process, including RAM and storage in swap files.
- [Resident set size](https://en.wikipedia.org/wiki/Resident_set_size) shows the total memory in RAM used by a process, including heap & stack.

Resident set size can underestimate because it doesn't include "memory" in swap files, but it can also overestimate if it includes memory used by shared libraries (so that shutting our process down wouldn't actually free up that memory, if others still use the library).
Virtual memory size overestimates, as it shows memory available to a process even when it isn't being used.

We can see the same information in `top` or `htop`, only now VSZ is called `VIRT` and RSS is called `RES`.
On windows VSZ is called `pagefile` and RSS is called `wset`.

Staying in Python, we can install `psutil` and use the [memory_info() method](https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_info) method of the [Process class](https://psutil.readthedocs.io/en/latest/#process-class).

```
import os

import psutil

def bytes(b):
    if b < 1024:
        print(f'{b} bytes')
    if b < 1048576:
        print(f'{round(b / 1024, 1)} kb')
    else:
        print(f'{round(b / 1048576, 1)} mb')


pid = os.getpid()
print(f'PID: {pid}')
info = psutil.Process(pid).mem_info()
print(b(info.vms))
print(b(info.rss))
input()
```

shows

```
PID: 186661
226.7 mb
11.7 mb
```

### resource

Like `psutil`, the `resource` module gets information from the operating system.
Unlike `psutil`, it's part of the standard library and focusses on the current process (`psutil` can tell you about any running process).

To get info on the current process, including all threads but no child processes, we can use [RUSAGE_SELF](https://docs.python.org/3/library/resource.html#resource.RUSAGE_SELF):

```
import resource
usage = resource.getrusage(resource.RUSAGE_SELF)
```

The returned object has [a number of fields](https://docs.python.org/3/library/resource.html#resource.getrusage) whose meaning is platform dependent and explained e.g. [here](https://manpages.debian.org/bullseye/manpages-dev/getrusage.2.en.html).
The list seems to have arisen historically, and contains a bunch of entries that aren't very usefull or even not filled in.
Here we'll focus on `max_rss`, which contains the **maximum resident set size** used by our process so far.

```
import resource
print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
```
shows e.g.
```
9928
```
On linux, this is in units of kilobyte (or kibibyte? I don't know).

### Garbage collection

Python uses [garbage collection](https://devguide.python.org/internals/garbage-collector/), and we can learn about the garbage collector's current state from the `gc` module.

Important things to know:

- Python's garbage collection keeps track of "non-atomic" objects, e.g. user-defined objects and lists, but not of simpler objects (e.g. ints).
- Python objects all maintain their own reference count. When the ref count of a simple (atomic) object hits zero, it will free its memory.
- More complex objects may not free their memory until the garbage collector is run.
- Instead of using e.g. `malloc` and `free` all the time, Python uses its own allocation and freeing methods, so that it can re-use a single block of memory. If more is needed Python asks for more. This means you won't see small memory leaks directly in your RSS.
- Some things are cached which you might not expect, for example: `x = 5; y = 5; x is y` returns `True` because Python caches the integer objects from -5 to 256 for re-use.

Less important:

- Objects tracked by `gc` are stored in one of three "generations".
- New objects are added to generation 0. If it survives a generation 0 garbage collection it will be moved to generation 1. If it survives a generation 1 run it gets moved to generation 2.

### tracemalloc

What about objects that are not managed by GC?
Since Python 3.4, we can track those using the standard library module `tracemalloc`.
This tracks where and when memory was allocated by Python.
You can use it to do clever things, like showing which objects are using memory, and where they were defined.

For some reason, I can't get it to work nicely.
See [case-2-tracemalloc-example.py](./case-2-tracemalloc-example.py).

### pympler

Pympler incorporates several tools including `muppy`, which seems to be the one we use here.
It can track all Python objects currently in use, and show you the ones that were added or removed since your last call.
This means we can track leaks of (certain!) Python objects with pympler.

In particular, Pympler seems to track (1) objects that are [tracked by `gc`](https://docs.python.org/3/library/gc.html#gc.is_tracked), and (2) objects that are referenced by objects that are tracked by `gc`.
I'm not sure that this is correct or the full story, see [case-2-tracemalloc-example.py](./case-2-tracemalloc-example.py).

However, it's a super useful tool to check if you're leaking Python objects.

Example:
```
#!/usr/bin/env python3
import pympler.tracker
tracker = pympler.tracker.SummaryTracker()

a = []

def side_effect():
    a.append([1.23] * 10)

for i in range(5):
    side_effect()
    tracker.print_diff()
    print()
```
Will show something like:
```
                   types |   # objects |    total size
======================== | =========== | =============
                    list |        3686 |     320.25 KB
                     str |        3667 |     254.99 KB
                     int |         820 |      22.43 KB
                    dict |           3 |     680     B
                    code |           1 |     246     B
   function (store_info) |           1 |     136     B
  function (side_effect) |           1 |     136     B
                    cell |           2 |      80     B
                 weakref |           1 |      72     B
                  method |           1 |      64     B
                   float |          -2 |     -48     B
                   tuple |         -38 |   -2696     B
                   
  types |   # objects |   total size
======= | =========== | ============
   list |           3 |    296     B
    str |           2 |    141     B
   code |           0 |     70     B
   
  types |   # objects |   total size
======= | =========== | ============
   list |           1 |    136     B
   
  types |   # objects |   total size
======= | =========== | ============
   list |           1 |    136     B
   
  types |   # objects |   total size
======= | =========== | ============
   list |           1 |    168     B
   code |           0 |    112     B
```
The first two entries show lots of memory allocated (or deallocated) in setting things up.
The remaining entries show a new list is created with every call to `side_effect`: a leak!

### Memory leaks?

What I think all of this means is that:

- `psutil` and `resource` won't pick up small leaks of Python objects straight away: changes in actual memory usage will be delayed until the Python-managed memory is full and gets increased.
- but `psutil` and `resource` are the only tools that pick up increases in memory _not handled by Python_.
- `pympler` can give us very detailed information about _some_ type of leaks.

## Investigation

Based on all this, I wrote a script called [mem.py](./mem.py) that runs repeated simulations, obtains stats using `psutil`, `resource`, `gc`, and `tracemalloc` and creates some graphs.

To see if it works, I manually added some memory leaks into the code for CVODES simulations (don't worry, I removed it again).

###

![img](a1-plain-50000-leaking-1-pyfloat-per-iteration.png)
![img](a2-plain-50000-leaking-empty-list-per-iteration.png)
![img](a3-plain-50000-leaking-1-double-per-iteration.png)
![img](a4-plain-50000-leaking-100-doubles-per-iteration.png)
![img](a5-plain-50000-no-deliberate-leak.png)
![img](b1-plain-500-leaking-1-pyfloat-per-iteration.png)
![img](b2-plain-500-leaking-1-empty-list-per-iteration.png)
![img](b3-plain-500-leaking-1-double-per-iteration.png)
![img](b4-plain-500-leaking-100-doubles-per-iteration.png)
![img](b5-plain-500-no-deliberate-leak.png)
![img](c3-plain-10000-leaking-1-double-per-iteration.png)













#
