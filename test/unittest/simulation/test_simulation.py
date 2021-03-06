# -*- coding: utf-8 -*-
"""
Tests of the analysis module
"""

# needed for python 3 compatibility
from __future__ import division

import os
import pickle
from neurotune.simulation.pype9 import NineLineSimulation
from neurotune.objective.spike import MinCurrentToSpikeObjective
from neurotune.algorithm import Algorithm
from neurotune.tuner import Tuner
from neurotune import Parameter
if __name__ == '__main__':
    from neurotune.utilities import DummyTestCase as TestCase  # @UnusedImport
else:
    try:
        from unittest2 import TestCase
    except ImportError:
        from unittest import TestCase


data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..', 'data', '9ml'))
nineml_file = os.path.join(data_dir, 'Golgi_Solinas08.9ml')
inactive_nineml_file = os.path.join(data_dir, 'Granule_DeSouza10.9ml')


# Create a non-abstract version of the base algorithm to initialise a Tuner
# object with
class DummyAlgorithm(Algorithm):
    pass


class TestNineLineSimulationConditions(TestCase):

    def test_injected_currents(self):
        simulation = NineLineSimulation(inactive_nineml_file)
        tuner = Tuner([Parameter('test', 'mS', 0.0, 1.0, False)],  # @UnusedVariable @IgnorePep8
                      MinCurrentToSpikeObjective(),
                      DummyAlgorithm(),
                      simulation)
        recordings = simulation.run_all([0.5])
        sig = recordings.segments[0].analogsignals[0]
        from matplotlib import pyplot as plt
        plt.plot(sig.times, sig)
        plt.show()
        print recordings


class TestNineLineSimulationPickle(TestCase):

    def test_pickle(self):
        simulation1 = NineLineSimulation(nineml_file)
        with open('./pickle', 'wb') as f:
            pickle.dump(simulation1, f)
        with open('./pickle', 'rb') as f:
            try:
                simulation2 = pickle.load(f)
            except ValueError:
                simulation2 = None
        os.remove('./pickle')
        self.assertEqual(simulation1, simulation2)


if __name__ == '__main__':
    test = TestNineLineSimulationConditions()
    test.test_injected_currents()
