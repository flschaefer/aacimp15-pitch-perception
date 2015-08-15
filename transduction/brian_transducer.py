from brian import *
from brian.hears import *

from transducer import Transducer


class BrianTransducer(Transducer):
    """
    A computational model of the human's hearing transduction stage, using the functionality of the brian library
    """

    def __init__(self):
        """
        Empty constructor. Fill with code if needed
        """
        pass

    def get_spikes(self, samples, sample_rate):
        cf = erbspace(20*Hz, 20*kHz, 300)
        sound = Sound(samples, samplerate=sample_rate*Hz)
        fb = Gammatone(sound, cf)
        output = fb.process()

        f = lambda x: 3 * clip(x, 0, Inf) ** (1.0/3.0)
        a = f(output)

        # Return spikes
        return a
