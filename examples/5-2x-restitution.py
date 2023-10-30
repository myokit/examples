class Restitution(object):
    """
    Can run a restitution experiment and return the values needed to make a
    plot.

    Accepts the following input arguments:

    ``model``
        The model for which to run the simulations
    ``vvar``
        The variable or variable name representing membrane potential. If not
        given, the method will look for the label ``membrane_potential``, if
        that's not found an exception is raised.

    """
    def __init__(self, model, vvar=None):
        # Check model
        self._model = model.clone()

        # Check membrane potential
        if vvar is None:
            self._vvar = self._model.label('membrane_potential')
            if self._vvar is None:
                raise ValueError(
                    'Membrane potential variable must be given by vvar or'
                    ' specified using the label "membrane_potential".')
        else:
            if isinstance(vvar, myokit.Variable):
                vvar = vvar.qname()
            elif '.' not in vvar:
                raise ValueError(
                    'The variable name vvar must be given as a fully qualified'
                    ' variable name <component.var>.')
            self._vvar = self._model.get(vvar)

        # Set default arguments
        self.set_max_step_size()
        self.set_times()
        self.set_beats()
        self.set_stimulus()
        self.set_threshold()

        # No data yet!
        self._data = None

    def _run(self):
        """
        Runs the simulations, saves the data.
        """
        # Create protocol
        e = {
            'level': self._stim_level,
            'start': 0,
            'duration': self._stim_duration,
            'period': self._clmin,
            'multiplier': 0,
        }

        # Create simulation
        s = myokit.Simulation(self._model)
        s.set_max_step_size(self._max_step_size)

        # Start testing
        i = 0
        pcls = []
        apds = []
        c = self._clmax
        while c >= self._clmin:
            # Update cycle length
            c = self._clmax - i * self._dcl
            i += 1

            # Create and set new protocol
            p = myokit.Protocol()
            e['period'] = c
            p.schedule(**e)
            s.set_protocol(p)

            # Run simulation
            s.reset()
            s.pre(c * self._pre_beats)
            d, a = s.run(
                c * self._beats,
                log=myokit.LOG_NONE,
                apd_variable=self._vvar,
                apd_threshold=self._apd_threshold
            )

            # Save apds
            for apd in a['duration']:
                pcls.append(c)
                apds.append(apd)

        # Store data
        self._data = pcls, apds

    def run(self):
        """
        Returns a :class:`DataLog` containing the tested cycle lengths as
        ``cl`` and the measured action potential durations as ``apd``. The
        diastolic intervals are given as ``di``.

        Each cycle length is repeated ``beats`` number of times, where
        ``beats`` is the number of beats specified in the constructor.
        """
        # Run
        if self._data is None:
            self._run()
        # Get data
        cl, apd = self._data
        d = myokit.DataLog()
        d['cl'] = list(cl)
        d['apd'] = list(apd)
        d['di'] = list(np.array(cl, copy=False) - np.array(apd, copy=False))
        return d

    def set_beats(self, beats=2, pre=50):
        """
        Sets the number of beats each cycle length is tested for.

        ``beats``
            The number of beats during which apd is measured
        ``pre``
            The number of pre-pacing beats done at each cycle length before the
            measurement.
        """
        beats = int(beats)
        pre = int(pre)
        if beats < 1:
            raise ValueError(
                'The number of beats must be an integer greater than zero.')
        if pre < 0:
            raise ValueError(
                'The number of pre-pacing beats must be a positive integer.')
        self._beats = beats
        self._pre_beats = pre
        self._data = None

    def set_max_step_size(self, dtmax=None):
        """
        Sets an (optional) maximum step size for the solver. To let the solver
        pick any step size it likes, use ``dtmax=None``.

        This method can be useful to avoid "CVODES flag 22" errors.
        """
        if dtmax is None:
            self._max_step_size = None
        else:
            dtmax = float(dtmax)
            if dtmax <= 0:
                raise ValueError(
                    'Maximum step size must be greater than zero.')
            self._max_step_size = dtmax
        self._data = None

    def set_stimulus(self, duration=2.0, level=1):
        """
        Sets the stimulus used to pace the model.

        ``stim_duration``
            The duration of the pacing stimulus.
        ``stim_level``
            The level of the dimensionless pacing stimulus.

        """
        duration = float(duration)
        level = float(level)
        if duration < 0:
            raise ValueError('The duratio cannot be negative.')
        self._stim_duration = duration
        self._stim_level = level
        self._data = None

    def set_threshold(self, threshold=-70):
        """
        Sets the APD threshold, specified as a fixed membrane potential.
        """
        self._apd_threshold = float(threshold)
        self._data = None

    def set_times(self, clmin=300, clmax=1200, dcl=20):
        """
        Sets the pacing cycle lengths tested in this experiment.

        ``clmin``
            The shortest cycle length tested.
        ``clmax``
            The longest cycle length tested.
        ``dcl``
            The size of the steps from ``clmin`` to ``clmax``

        """
        clmin = float(clmin)
        clmax = float(clmax)
        dcl = float(dcl)
        if clmin < 0:
            raise ValueError('Minimum time cannot be negative.')
        if clmin >= clmax:
            raise ValueError('Minimum time must be smaller than maximum time.')
        if dcl <= 0:
            raise ValueError('Step size must be greater than zero')
        self._clmin = clmin
        self._clmax = clmax
        self._dcl = dcl
        self._data = None

