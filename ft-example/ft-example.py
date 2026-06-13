#!/usr/bin/env python3
#
# FiberTissueSimulation example
#
import sys
import myokit

debug = 'debug' in sys.argv

# Load models
mf = myokit.load_model('stewart-2009.mmt')
mt = myokit.load_model('tentusscher-2006-lhopital.mmt')

# Create a protocol
p = myokit.pacing.blocktrain(period=1000, duration=2)

# Set up a simulation
s = myokit.FiberTissueSimulation(
    mf,
    mt,
    p,
    ncells_fiber=(32, 2),
    ncells_tissue=(32, 32),
    nx_paced=5,
    g_fiber=(3, 1),
    g_tissue=(3, 1),
    g_fiber_tissue=3,
)
s.set_step_size(0.0005)

# Debugging? Then log all variables
if debug:
    logf = logt = myokit.LOG_STATE + myokit.LOG_BOUND
else:
    logf = ['engine.time', 'membrane.V', 'calcium.Ca_i']
    logt = ['engine.time', 'membrane.V', 'calcium.Cai']

# Run (using a progress printer to see how far we got)
pr = myokit.ProgressPrinter()
df, dt = s.run(50, logf=logf, logt=logt, log_interval=0.5, progress=pr)
if debug:
    print('Sim OK!')
    sys.exit(1)

# Convert the dictionary logs to structured 2d arrays
bf = df.block2d()
bt = dt.block2d()

# Create a combined data block
# First define a map that indicates equivalent variables. Format:
# new_name : (modelf name, modelt name, padding value)
varmap = {
    'V' : ('membrane.V', 'membrane.V', -100),
    'Cai': ('calcium.Ca_i', 'calcium.Cai', 0),
}
b = myokit.DataBlock2d.combine(bf, bt, map2d=varmap, pos1=(0, 15))

# Store the data block
fname = 'combined.zip'
print(f'Storing in {fname}')
b.save(fname)

print('Done!')
print('View with: python3 -m myokit block combined.zip')

