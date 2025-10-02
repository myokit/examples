# Work in progress!

*This page lists the planned jupyter notebook-based examples. In time this will replace [the current example page](http://myokit.org/examples/) at myokit.org.*

## Using Myokit

These example notebooks show how [Myokit](http://myokit.org) can be used in a variety of cardiac electrophysiology applications, at the cellular, sub-cellular, or tissue scale.
They accompany the detailed information on the individual classes and methods found in the [API documentation](https://myokit.readthedocs.io).
Software developers may also want to check out Myokit's [github repository](https://github.com/myokit/myokit/).

### Before you begin

1. **How to use these notebooks**: If you're not sure how to use these examples, start here.
   [![View on github](img/github.svg)](examples/0-1-before-you-begin.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/examples/0-1-before-you-begin.ipynb)

2. **Installation instructions**: These are currently at http://myokit.org/install, but will be moved here eventually.

3. **Quick start guide**: This section will provide quick start guide based on real life examples, without going into technical detail. For users who prefer to jump in at the deep end! Will be based on [existing tutorials](http://myokit.org/tutorial/). Most likely there will be 1 to 3 quick start guides, each on a different topic, letting users jump straight into their area of interest. A 4th should very quickly show how the basics discussed in 3.4, 3.6, and 8 to help make your published code more reproducible.

## 1. Running simulations

1. **Simulating an action potential**: Covers loading a model, protocol, and script; creating a simulation; running a simulation; plotting simulation results with matplotlib.
   [![View on github](img/github.svg)](examples/1-1-simulating-an-action-potential.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/examples/1-1-simulating-an-action-potential.ipynb)

2. **Logging simulation results**: Selecting variables by name or using logging flags; Logging derivatives of state variables; Continuing on from a previous simulation; Selecting which points to log; Storing results to disk.
   [![View on github](img/github.svg)](examples/1-2-logging-simulation-results.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/examples/1-2-logging-simulation-results.ipynb)

3. **Starting, stopping, pre-pacing, and loops**: Starting and stoppping simulations; Pre-pacing to a "steady state"; Simulating the effects of parameter changes.
   [![View on github](img/github.svg)](examples/1-3-starting-stopping.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/examples/1-3-starting-stopping.ipynb)

4. Controlling the solver
    - [ ] Simulation errors
    - [ ] Absolute and relative tolerance
    - [ ] Max time step

5. Discontinuities
    - [ ] Plotting discontinuities
    - [ ] Using protocols tells the solver about discontinuities
    - [ ] Not using protocols? Max time step
    - [ ] TimeSeriesProtocols interpolate!

7. Root-finding and sensitivities
    - [ ] Tracking an action potential duration
    - [ ] Obtaining sensitivities

## 2. Using the IDE

1. **Exploring models in the IDE**: Starting the IDE; Using the Explorer; Graphing model structure; Getting information about variables; Running embedded scripts.
   [![View on github](img/github.svg)](examples/2-1-exploring-models-in-the-ide.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/examples/2-1-exploring-models-in-the-ide.ipynb)

2. Creating protocols in the IDE
    - [ ] MMT syntax, link to full
    - [ ] Plotting
    - [ ] Models without pacing (Purkinje)

3. **Running scripts in the IDE**:
   Briefly discusses running embedded scripts, and the pros and cons of this feature.
   [![View on github](img/github.svg)](examples/2-3-running-scripts-in-the-ide.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/examples/2-3-running-scripts-in-the-ide.ipynb)

## 3. Working with models

1. Model syntax: a brief overview
    - [ ] Model, components, variables
    - [ ] Units (variable and expression units)
    - [ ] Annotations (bindings, labels, meta data)

2. Implementing models
    - [ ] Validating the model structure
    - [ ] Verifying model output with step (from code, against stored from other data, against other mmt files from command line)
    - [ ] Checking model units

3. Units
    - [ ] Unit objects
    - [ ] Predefined units
    - [ ] Quantities
    - [ ] Unit conversion
    - [ ] Representations?

4. Creating and manipulating models from the API
    - [ ] Create model, add component, variables, equations, units, labels
    - [ ] Promoting/demoting, state order
    - [ ] Validation 
    - [ ] Note: API allows you to build invalid models, by design
    - [ ] Note: Myokit is not a CAS (`x = x-x` is cyclical, `x=y/y` depends on y, `dot(x) = 0; y=dot(x)` makes y depend on x and t)   
    - [ ] Moving (and renaming)
    - [ ] Importing components?
    - [ ] Differentiation? Init() type

5. Querying models
    - [ ] Info about variables
    - [ ] Info about variable evaluation
    - [ ] Dependency stuff? Graphs?
    - [ ] Getting/graphing functions with pyfunc

6. Working with multiple models
    - [ ] Identifying common variables with annotations
    - [ ] A shared ontology?
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

## 5. Single-cell simulations

1. Protocols for periodic pacing
    - [ ] MMT syntax, link to full
    - [ ] API
    - [ ] pacing factories
    - [ ] AP clamp --> interpolation!
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
    - [ ] Data clamp (AP clamp) --> do not use for discontinuous!

X. Analysing results
    - [ ] Splitting, trimming, etc
    - [ ] Comparing with real data? (also: sweeps etc.!)

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

0. Link to [artefacts notebooks](https://github.com/CardiacModelling/fitting-notebooks/tree/artefacts/artefacts)

## 7. Multi-cell simulations

1. Simulating strands and tissue
    - [ ] 1d, no OpenCL, binding
    - [ ] 1d, OpenCL
    - [ ] OpenCL info & select
    - [ ] 2d, OpenCL
    - [ ] Interdependent components example: CellML import of Courtemanche

2. Viewing multi-cell simulation results
    - [ ] Storing CSV log
    - [ ] Converting to block
    - [ ] Writing block (txt vs zip)
    - [ ] Displaying with DataBlock viewer
    - [ ] Movies

3. Setting the step size
    - [ ] Foward Euler method
    - [ ] Convergence analysis
    - [ ] Rush & Larsen's method
    - [ ] Bigger & better

4. Running and debugging simulations
    - [ ] Using a progress reporter
    - [ ] Using find_nan (automatically)
    - [ ] Step sizes!
    - [ ] l'hopital's rule (link to Maurice)
    - [ ] precision and native maths
    
5. Simulating with heterogeneity
    - [ ] Heterogeneity in parameters (scalar field, NxN)
    - [ ] Heterogeneity in conductance (scalar field N-1xN-1)
    - [ ] With different cell types (scalar field!)

6. Simulating arbitrary geometries
    - [ ] set_connections
  
## X. Working with data

1. Using patch clamp data
    - [ ] Importing patch clamp data: native interface and conversion to log
    - [ ] Importing patch clamp meta data (native & in log)
    - [ ] DataLog viewer
    - [ ] Importing protocols from ABF and HEKA
    - [ ] Exporting patch clamp protocols? (ATF)
    - [ ] Sweeps etc.

## 8. Publishing your Myokit work

1. Tactics for reproducibility
    - [ ] One file per figure (or other result)
    - [ ] One `mmt` file per model - or no new model code at all! --> link back to Working with multiple models
    - [ ] What to include (mention MIASE and MICEE), but also Myokit version no., Python version no. Sundials version no. Show how to get from `myokit system` command

2. "Freezing dependencies"
    - [ ] Using virtual environments (1, with conda; 2, with virtualenv)
    - [ ] Using docker

3. Github and Zenodo
   - [ ] Getting a DOI for your model code

4. Uploading a model to PMR
    - [ ] CellML export
    - [ ] Editing/annotation in COR, if desired?
    - [ ] https://github.com/CardiacModelling/cellml-repo-updates

## Appendix

0. Using Matplotlib, see https://myokit.readthedocs.io/en/stable/guide/matplotlib.html
    - [ ] Base on from https://myokit.readthedocs.io/en/stable/guide/matplotlib.html
    - [ ] Show simple example, but with axes etc.
    - [ ] Then with subplots, and subplots_adjust
    - [ ] Then with gridspec
    - [ ] Then stop.
    - [ ] Alternatively replace this whole section with a link to https://github.com/MichaelClerx/making-figures/

0. Using NumPy
    - [ ] Discuss log.npview() ?
    - [ ] Just show an example
    - [ ] And link to https://docs.scipy.org/doc/numpy/user/numpy-for-matlab-users.html

0. Using Myokit from the command line

0. Profiling CVODE(s) simulations
    - [ ] It's probably logging (explain why, make graphs, reduce n vars, explain about "oversampling" = lots of interpolation)
    - [ ] Using `myokit.run` and the `DEBUG_x` switches

0. Developing Myokit
    - [ ] Yes please!
    - [ ] Github issues
    - [ ] Contributing.md (includes code layout)
    - [ ] Technical notes

## Technical notes

This section contains notebooks that explain or define some of the trickier parts in Myokit.
They are used in Myokit development, and document tricky decisions made along the way.
These notebooks have not been reviewed or checked extensively, so some errors may be present.

1. **Pacing**
   [![View on github](img/github.svg)](technical-notes/1-1-pacing.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/1-1-pacing.ipynb)
2. **Logging**
   [![View on github](img/github.svg)](technical-notes/1-2-logging.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/1-2-logging.ipynb)
3. **CVODE(s) single-cell simulations**
   [![View on github](img/github.svg)](technical-notes/1-3-cvodes-simulation.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/1-3-cvodes-simulation.ipynb)
4. **OpenCL multi-cell simulations**
   [![View on github](img/github.svg)](technical-notes/1-4-opencl-simulation.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/1-4-opencl-simulation.ipynb)
5. **HH channel models**
   [![View on github](img/github.svg)](technical-notes/1-5-hh-channels.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/1-5-hh-channels.ipynb)
6. **Markov channel models**
   [![View on github](img/github.svg)](technical-notes/1-6-markov-channels.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/1-6-markov-channels.ipynb)
7. **Rush-Larsen updates**
   [![View on github](img/github.svg)](technical-notes/1-7-rush-larsen.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/1-7-rush-larsen.ipynb)

### Simulation test cases
   
1. **Simple model**
  [![View on github](img/github.svg)](technical-notes/2-1-test-case-simple.ipynb)
  [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/2-1-test-case-simple.ipynb)
2. **Simulation test case: HH ion channel model**
  [![View on github](img/github.svg)](technical-notes/2-2-test-case-hh-current.ipynb)
  [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/2-2-test-case-hh-current.ipynb)
3. **Simulation test case: PK model with sensitivities**
  [![View on github](img/github.svg)](technical-notes/2-3-test-case-pk-model.ipynb)
  [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/2-3-test-case-pk-model.ipynb)
4. **Simulation test case: Logistic model with parameters in initial conditions**
  [![View on github](img/github.svg)](technical-notes/2-4-test-case-logistic-model.ipynb)
6. **Autodiff simulations**
  [![View on github](img/github.svg)](technical-notes/2-x-autodiff.ipynb)
  [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/2-x-autodiff.ipynb)

### Python details 

1. **Float precision, units, and pacing**
   [![View on github](img/github.svg)](technical-notes/3-1-floats-units-and-pacing.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/3-1-floats-units-and-pacing.ipynb)
2. **Equality, hashes & pickling**
   [![View on github](img/github.svg)](technical-notes/3-2-equality-hashes-and-pickling.ipynb)
   [![View on nbviewer](img/nbviewer.svg)](https://nbviewer.jupyter.org/github/myokit/myokit-examples/blob/main/technical-notes/3-2-equality-hashes-and-pickling.ipynb)
3. **Memory leaks**
   [![View with github Markdown viewer](img/github.svg)](technical-notes/3-3-memory-leaks/README.md)

## Myokit publications

- PBMB examples (http://github.com/myokit/pbmb-2016)

## Tutorials

- Hand-outs EWGCCE 2014 (http://myokit.org/tutorial/)
- Hand-outs CINC 2018 (http://myokit.org/tutorial/)

## Contributors

These examples, tutorials and technical notes were created by Michael Clerx, with contributions from David Augustin and Enno de Lange, and feedback from several others.

## License and re-use

Please:

- Re-use the example code in the notebooks (.ipynb) and separate python (.py) files as much as you like.
- Contact michael@myokit.org if you wish to re-use the notebook text or any figures included in this repository.
- Check the included model files for information about their copyright and licensing.

