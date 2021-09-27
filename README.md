# Work in progress!

*More examples can be found on:* http://myokit.org/examples/

## Using Myokit

These example notebooks show how Myokit can be used in a variety of cardiac electrophysiology applications, at the cellular, sub-cellular, or tissue scale.
They accompany the detailed Myokit (API) documentation provided on [https://myokit.readthedocs.io](https://myokit.readthedocs.io).

- [Before you begin](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/0-1-before-you-begin.ipynb)
  : If you're not sure how to use these examples, start here.

## 1. Running simulations

1. [Simulating an action potential](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/1-1-simulating-an-action-potential.ipynb)
   : Covers loading a model, protocol, and script; creating a simulation; running a simulation; plotting simulation results with matplotlib.

2. [Logging simulation results](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/1-2-logging-simulation-results.ipynb)
   : Selecting variables by name or using logging flags; Logging derivatives of state variables; Continuing on from a previous simulation; Selecting which points to log; Storing results to disk.

3. [Starting, stopping, pre-pacing, and loops](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/1-3-starting-stopping.ipynb)
   : Starting and stoppping simulations; Pre-pacing to a "steady state"; Simulating the effects of parameter changes.

4. Controlling the solver
    - [ ] Simulation errors
    - [ ] Absolute and relative tolerance
    - [ ] Max time step

5. Root-finding and sensitivities
    - [ ] Tracking an action potential duration
    - [ ] Obtaining sensitivities

## 2. Using the IDE

1. [Exploring models in the IDE](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/2-1-exploring-models-in-the-ide.ipynb)
    - Starting the IDE
    - Using the Explorer
    - Graphing model structure
    - Getting information about variables
    - Running embedded scripts

2. Creating protocols in the IDE
    - [ ] MMT syntax, link to full
    - [ ] Plotting
    - [ ] Models without pacing (Purkinje)


## 3. Working with models

1. Model syntax: a brief overview
    - [ ] Model, components, variables
    - [ ] Units (variable and expression units)
    - [ ] Annotations (bindings, labels, meta data)

2. Implementing models
    - [ ] Validation
    - [ ] Comparing models with step
    - [ ] Unit checking

3. Modifying models using the API
    - [ ] Adding variables
    - [ ] Getting functions with pyfunc
    - [ ] Manipulating models
    - [ ] Manipulating equations (variable, eq, lhs, rhs, derivatives, refs_by, refs_to)

4. Units
    - [ ] Unit objects
    - [ ] Predefined units
    - [ ] Quantities
    - [ ] Unit conversion

5. Working with multiple models
    - [ ] Identifying common variables
    - [ ] Unit conversion
    - [ ] "Clamping" a variable
    - [ ] Importing components

## 4. Importing and exporting

1. Using CellML
    - [ ] Importing
    - [ ] Exporting
    - [ ] Auto stimulus, vs hardcoded
    - [ ] Annotations
    - [ ] Using APIs

2. Using other model formats
    - [ ] SBML
    - [ ] ChannelML
    - [ ] easyml, stan

3. Exporting runnable code
    - [ ] matlab, C, C++, python
    - [ ] opencl, cuda
    - [ ] Import isn't possible

4. Exporting presentation formats
    - [ ] Exporting for presentations: latex / html

5. Using data formats
    - [ ] Importing patch clamp data
    - [ ] DataLog viewer
    - [ ] Importing protocols from ABF
    - [ ] Exporting patch clamp protocols? (ATF)

## 5. Single-cell simulations

1. Protocols for periodic pacing
    - [ ] MMT syntax, link to full
    - [ ] API
    - [ ] pacing factories
    - [ ] AP clamp
    - [ ] Models without pacing (Purkinje)

2. Calculating APDs
    - [ ] APD calculation
    - [ ] Restitution
    - [ ] Alternans

0. Pre-pacing to steady state

0. Analysing currents
    - [ ] Cumulative current plots
    - [ ] More things from lib.plots ?

0. Strenght-duration curves

## 6. Ion current simulations

1. Voltage-step protocols
    - [ ] Creating a step protocol in mmt (``next``)
    - [ ] Plotting it (fitting tutorial!)
    - [ ] is_sequence etc,
    - [ ] with add_step
    - [ ] with pacing factory
    - Link to fitting tutorial. Or even move those bits here?

2. Applying complex waveforms
    - [ ] Steps and ramps
    - [ ] Steps and sine waves
    - [ ] Data clamp (AP clamp)

3. Hodgkin-Huxley models
    - [ ] CVODES sim
    - [ ] Isolating HH models
    - [ ] Analytical simulation
    - [ ] Converting HH model forms

4. Markov models
    - [ ] Isolating markov models
    - [ ] Analytical simulation
    - [ ] Discrete simulation

0. Examples of fitting ionic currents and fitting conductances: [ion channel fitting notebooks](https://github.com/CardiacModelling/fitting-notebooks)

## 7. Multi-cell simulations

0. Simulating strand and tissue
    - [ ] 1d, no OpenCL, binding
    - [ ] Step size!
    - [ ] 1d, OpenCL
    - [ ] OpenCL info & select
    - [ ] Setting step size (convergence)
    - [ ] 2d, OpenCL

0. Viewing multi-cell simulation results
    - [ ] Storing CSV log
    - [ ] Converting to block
    - [ ] Writing block (txt vs zip)
    - [ ] Displaying with DataBlock viewer
    - [ ] Movies

0. Running simulations
    - [ ] Setting step sizes again!
    - [ ] Using find_nan (automatically)
    - [ ] Using a progress reporter

0. Simulating with heterogeneity
    - [ ] Scalar field
    - [ ] With different cell types (field approach)
    - [ ] Conductance field

0. Simulating arbitrary networks
    - [ ] set_connections

## Appendix

0. Matplotlib basics, see https://myokit.readthedocs.io/en/stable/guide/matplotlib.html
    - [ ] Base on from https://myokit.readthedocs.io/en/stable/guide/matplotlib.html
    - [ ] Show simple example, but with axes etc.
    - [ ] Then with subplots, and subplots_adjust
    - [ ] Then with gridspec
    - [ ] Then stop.

0. Using numpy
    - [ ] Discuss log.npview() ?
    - [ ] Just show an example
    - [ ] And link to https://docs.scipy.org/doc/numpy/user/numpy-for-matlab-users.html

0. Developing Myokit
    - [ ] Yes please!
    - [ ] Github issues
    - [ ] Contributing.md (includes code layout)
    - [ ] Technical notes

## Technical notes

This section contains notebooks that explain or define some of the trickier parts in Myokit.
They are used in Myokit development, and document tricky decisions made along the way.
These notebooks have not been reviewed or checked extensively, so some errors may be present.

1. [Pacing](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/t1-pacing.ipynb)
2. [Logging](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/t2-logging.ipynb)
3. [CVODE(s) single-cell simulations](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/t3-cvodes-simulation.ipynb)
4. [OpenCL multi-cell simulations](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/t4-opencl-simulation.ipynb)
5. [HH channel models](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/t5-hh-channels.ipynb)
6. [Markov channel models](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/t6-markov-channels.ipynb)
7. [Rush-Larsen updates](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/t7-rush-larsen.ipynb)

- [Simulation test case: Simple model](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/tA-test-case-simple.ipynb)
- Simulation test case: HH ion channel model
- [Simulation test case: PK model](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/tC-test-case-pk-model.ipynb)
- [Autodiff simulations](https://nbviewer.jupyter.org/github/MichaelClerx/myokit-examples/blob/main/tZ-autodiff.ipynb)

## Contributors

These examples and technical notebooks were created by Michael Clerx, with contributions from David Augustin, and feedback from several others.

## License and re-use

Please:

- Re-use the example code in the notebooks (.ipynb) and separate python (.py) files as much as you like.
- Contact michael@myokit.org if you wish to re-use the notebook text or any figures included in this repository.
- Check the included model files for information about their copyright and licensing.

