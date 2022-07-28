#!/usr/bin/env python3
#
#
#
import gc
import os
import resource
import sys
import tracemalloc

import myokit
import psutil
import pympler.tracker

import matplotlib.pyplot as plt
import numpy as np


def test(command, repeats, use_pympler=False, init_gc=True, force_gc=False):

    print(f'Testing with {command}, {repeats} repeats')
    print('Initial GC' if init_gc else 'No initial GC')
    print('Continuous GC' if force_gc else 'Automatic GC')

    # Get and show pid
    pid = os.getpid()
    print(f'PID: {pid}')

    # Get command
    print('Loading test case')
    name = command
    command = case(name)

    # Create lists
    ind = np.arange(1, 1 + repeats)
    vms = np.zeros(repeats)
    rss = np.zeros(repeats)
    mxr = np.zeros(repeats)
    nob = np.zeros(repeats)
    nc1 = np.zeros(repeats)
    nc2 = np.zeros(repeats)
    nc3 = np.zeros(repeats)
    tm1 = np.zeros(repeats)
    tm2 = np.zeros(repeats)

    # Set up, fill caches
    print('Getting process in psutil')
    p = psutil.Process(pid)
    nob[0] = len(gc.get_objects())
    stats = gc.get_stats()

    # Flush pympler stuff
    if use_pympler:
        print('Loading pympler tracker')
        tracker = pympler.tracker.SummaryTracker()
        stdout = sys.stdout
        sys.stdout = None
        command()
        tracker.print_diff()
        tracker.print_diff()
        sys.stdout = stdout

    # Collect garbage so far
    if init_gc:
        gc.collect()

    # Start tracemalloc
    tracemalloc.start()
    mac = tracemalloc.get_traced_memory()
    tm1[0] = mac[0] #- tracemalloc.get_tracemalloc_memory()
    tm2[0] = mac[1]

    # Run
    print('Running')
    for i in range(repeats):
        if use_pympler:
            tracker.diff()
        command()
        if force_gc:
            gc.collect()

        if use_pympler:
            print()
            tracker.print_diff()
        elif not i % 100:
            print('.', end='')
            sys.stdout.flush()

        mem = p.memory_info()
        vms[i] = mem.vms
        rss[i] = mem.rss
        mxr[i] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        nob[i] = len(gc.get_objects())
        stats = gc.get_stats()
        nc1[i] = stats[0]['collections']
        nc2[i] = stats[1]['collections']
        nc3[i] = stats[2]['collections']
        mac = tracemalloc.get_traced_memory()
        tm1[i] = mac[0] #- tracemalloc.get_tracemalloc_memory()
        tm2[i] = mac[1]

    if not use_pympler:
        print('')

    # Figure
    ds = 'steps-pre'
    fig = plt.figure(figsize=(8, 10))
    fig.subplots_adjust(0.1, 0.04, 0.99, 0.99, wspace=0.4, hspace=0.5)
    grid = fig.add_gridspec(6, 2)

    ax = fig.add_subplot(grid[0, 0])
    ax.set_ylabel('VMS (mib)')
    ax.plot(ind, vms / 2**20, ds=ds)
    ax = fig.add_subplot(grid[0, 1])
    ax.set_ylabel('$\Delta$ VMS (kib)')
    ax.plot(ind, (vms - vms[0]) / 1024, ds=ds)

    ax = fig.add_subplot(grid[1, 0])
    ax.set_ylabel('RSS (mib)')
    ax.plot(ind, rss / 2**20, ds=ds)
    ax = fig.add_subplot(grid[1, 1])
    ax.set_ylabel('$\Delta$ RSS (kib)')
    ax.plot(ind, (rss - rss[0]) / 1024, ds=ds)

    ax = fig.add_subplot(grid[2, 0])
    ax.set_ylabel('max RSS (mib)')
    ax.plot(ind, mxr / 2**10, ds=ds)
    ax = fig.add_subplot(grid[2, 1])
    ax.set_ylabel('$\Delta$ max RSS (kib)')
    ax.plot(ind, (mxr - mxr[0]), ds=ds)

    ax = fig.add_subplot(grid[3, 0])
    ax.set_ylabel('GC objects')
    ax.plot(ind, nob, ds=ds)
    ax = fig.add_subplot(grid[3, 1])
    ax.set_ylabel('$\Delta$ GC obj.')
    ax.plot(ind, nob, ds=ds)

    ax = fig.add_subplot(grid[4, 0])
    ax.set_ylabel('GC collects')
    ax.plot(ind, nc1, ds=ds)
    ax.plot(ind, nc2, ds=ds)
    ax.plot(ind, nc3, ds=ds)
    ax = fig.add_subplot(grid[4, 1])
    ax.set_ylabel('$\Delta$ GC coll.')
    ax.plot(ind, nc1 - nc1[0], ds=ds)
    ax.plot(ind, nc2 - nc2[0], ds=ds)
    ax.plot(ind, nc3 - nc3[0], ds=ds)

    ax = fig.add_subplot(grid[5, 0])
    ax.set_ylabel('Tracemalloc peak (kib)')
    ax.plot(ind, tm2 / 1024, ds=ds)
    ax = fig.add_subplot(grid[5, 1])
    ax.set_ylabel('Tracemalloc cur. (kib)')
    ax.plot(ind, tm1 / 1024, ds=ds)

    name = f'{name}-{repeats}'
    if force_gc:
        name += '-continuous-gc'
    if not init_gc:
        name += '-no-initial-gc'
    print(f'Writing result to {name}')
    plt.savefig(name + '.png')
    plt.show()


def case(name='plain'):
    # Return a simulation method
    m, p, _ = myokit.load('example')

    sens = (
        ('ina.m', 'dot(ina.m)', 'ina.INa'),
        ('ina.gNa', 'init(ina.m)')
    )

    if name == 'plain':
        s = myokit.Simulation(m, p)

        def c():
            s.run(10)

    elif name == 'sens':
        s = myokit.Simulation(m, p, sens)

        def c():
            s.run(10)

    elif name == 'realtime':
        # Realtime tracking
        # Note: This doesn't show much: Python re-uses strings etc. so can
        # delete some decrefs without seeing it here!
        v = m.get('engine').add_variable('realtime')
        v.set_rhs(0)
        v.set_binding('realtime')
        s = myokit.Simulation(m, p)

        def c():
            s.run(10)

    elif name == 'apd':
        # APD measuring
        # Note: Can remove some decrefs without seeing results here...
        s = myokit.Simulation(m, p)

        def c():
            s.run(1000, apd_variable='membrane.V', apd_threshold=-1)

    elif name == 'log_times':
        # Point-list logging
        s = myokit.Simulation(m, p, sens)
        lt = list(range(0, 1000, 10))

        def c():
            s.reset()
            s.run(1000, log_times=lt)

    elif name == 'log_times_np':
        # Point-list logging
        s = myokit.Simulation(m, p, sens)
        import numpy as np
        lt = np.arange(0, 2, 10)

        def c():
            s.reset()
            s.run(20, log_times=lt)

    else:
        raise ValueError(f'Unknown test: simulation {name}')

    return c


test('plain', 500, init_gc=True, force_gc=False)

