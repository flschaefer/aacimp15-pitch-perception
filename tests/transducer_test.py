from brian import *
from brian.hears import *


class TransducerTest(object):
    @staticmethod
    def run_tests(transducer):
        TransducerTest.test_transducer_output(transducer)

    @staticmethod
    def test_transducer_output(transducer):
        # Create simple sound for testing purposes
        test_sound = tone(0.5 * kHz, .1 * second)  # TODO: Remove Brian dependency

        # Create nerve activity from test sound
        spikes = transducer.get_spikes(test_sound)

        # Make sure transducer output has the right format
        assert len(spikes) == 300
        assert min(spikes) >= 0
