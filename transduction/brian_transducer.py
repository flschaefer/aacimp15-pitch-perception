from brian import *
from brian.hears import *

from transducer import Transducer

import numpy as np


class BrianTransducer(Transducer):
    """
    A computational model of the human's hearing transduction stage, using the functionality of the brian library
    """

    def __init__(self, n_channels=3000.):
        self.n_channels = n_channels

    def get_spikes(self,samples, sample_rate):

        cf = erbspace(20*Hz, 20*kHz, self.n_channels)

        sound = Sound(samples, samplerate=sample_rate*Hz)

        fb = Gammatone(sound, cf)
        output = fb.process()

        f = lambda x: 3 * clip(x, 0, Inf) ** (1.0/3.0)
        a = f(output)
        ihc = FunctionFilterbank(fb, lambda x: 3*clip(x, 0, Inf)**(1.0/3.0))

        eqs = '''
        dv/dt = (I-v)/(1*ms)+0.2*xi*(2/(1*ms))**.5 : 1
        I : 1
        '''

        anf = FilterbankGroup(ihc, 'I', eqs, reset=0, threshold=1, refractory=5*ms)
        M = SpikeMonitor(anf)

        return M.spikes


if __name__ == '__main__':


    sample_rate = 44100

    sound1 = tone(1*kHz, .1*second)
    sound2 = whitenoise(.1*second)
    sound = sound1+sound2
    sound = sound.ramp()
    samples = np.array(sound)

    transducer = BrianTransducer()

    s = transducer.get_spikes(samples,sample_rate)

    print s
