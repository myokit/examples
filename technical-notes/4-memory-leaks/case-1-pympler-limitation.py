#!/usr/bin/env python3
#
# This is an example of tracking Python objects with Pympler.
#
# As far as I understand (https://github.com/pympler/pympler/issues/152),
# Pympler looks at objects tracked by the garbage collector (GC), or linked
# from objects tracked by GC. This does not include primitives (floats,
# doubles) or empty dictionaries (for some reason).
#
# In my tests, pympler will detect when a C extension creates a list and
# doesn't decref it. But it does detect the same for a float.
#
# In the script below, I try something similar in pure Python. I feel like
# pympler should still know about the int and float (from globals()) but it
# doens't seem to.
#
import gc
import sys

import pympler.tracker

# Create tracker
tracker = pympler.tracker.SummaryTracker()

n1 = n2 = 0

# Re-route stdout and perform first two calls: this gets rid of memory used by
# imports etc.
stdout = sys.stdout
sys.stdout = None
tracker.print_diff()
n_gc = len(gc.get_objects())
tracker.print_diff()
sys.stdout = stdout

print(f'1. Objects tracked by GC, since first count: {len(gc.get_objects()) - n_gc}')
a = 5
b = 1.2
c = []
d = {}
print()
tracker.print_diff()            # Show difference
print()
print(f'2. Objects tracked by GC, since first count: {len(gc.get_objects()) - n_gc}')

# Add object to list
c.append(4)

print()
tracker.print_diff()            # Show difference
print()
print(f'3. Objects tracked by GC, since first count: {len(gc.get_objects()) - n_gc}')

print(globals())
