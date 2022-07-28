#!/usr/bin/env python3
#
# This is an example of tracking memory usage with tracemalloc.
#
#
import gc
import sys
import tracemalloc

# Start tracemalloc
tracemalloc.start()

# Currently used memory
tracemalloc.clear_traces()
s1 = tracemalloc.take_snapshot()
#a = 123123
s2 = tracemalloc.take_snapshot()
n_gc = len(gc.get_objects())
print()
print('Did nothing')
print(f'Objects tracked by GC, since first count: {len(gc.get_objects()) - n_gc}')
print(f'Memory tracked: {tracemalloc.get_traced_memory()[0]}')
for x in s2.compare_to(s1, 'filename'):
    print(x)
print()

tracemalloc.clear_traces()
s1 = tracemalloc.take_snapshot()
a = 1234567892345
s2 = tracemalloc.take_snapshot()
print()
print('Created a big int')
print(f'Objects tracked by GC, since first count: {len(gc.get_objects()) - n_gc}')
print(f'Memory tracked: {tracemalloc.get_traced_memory()[0]}')
for x in s2.compare_to(s1, 'filename'):
    print(x)

tracemalloc.clear_traces()
s1 = tracemalloc.take_snapshot()
b = []
s2 = tracemalloc.take_snapshot()
print()
print('Made an empty list')
print(f'Objects tracked by GC, since first count: {len(gc.get_objects()) - n_gc}')
print(f'Memory tracked: {tracemalloc.get_traced_memory()[0]}')
for x in s2.compare_to(s1, 'filename'):
    print(x)

tracemalloc.clear_traces()
s1 = tracemalloc.take_snapshot()
b = [0] * 1000
s2 = tracemalloc.take_snapshot()
print()
print('Made a big list')
print(f'Objects tracked by GC, since first count: {len(gc.get_objects()) - n_gc}')
print(f'Memory tracked: {tracemalloc.get_traced_memory()[0]}')
for x in s2.compare_to(s1, 'filename'):
    print(x)
