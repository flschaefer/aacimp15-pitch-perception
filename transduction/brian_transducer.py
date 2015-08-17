from brian import *
from brian.hears import *

from transducer import Transducer

import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import kaiserord, lfilter, firwin, freqz


class BrianTransducer(Transducer):
    """
    A computational model of the human's hearing transduction stage, using the functionality of the brian library
    """

    def __init__(self, n_channels=300.):
        self.n_channels = n_channels

    def get_spikes(self,samples, sample_rate):

        cf = erbspace(100*Hz, 8*kHz, self.n_channels)

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
        run(sound.duration)
        return M.spikes

    def get_cochleogram(self,samples, sample_rate):

        cf = erbspace(100*Hz, 8*kHz, self.n_channels)
        # Hair cells transduction parameters (low pass filter)
        width_hz = 3000.0
        # The desired attenuation in the stop band, in dB.
        ripple_db = 60.0
        # The cutoff frequency of the filter.
        cutoff_hz = 1000.0

        taps = kaiser_design(sample_rate, width_hz, ripple_db, cutoff_hz)

        sound = Sound(samples, samplerate=sample_rate*Hz)
        fb = Gammatone(sound, cf)
        f = lambda x: 3 * clip(x, 0, Inf) ** (1.0/3.0)
        lphwr =  filtered_x = lfilter(taps, 1.0, f(fb.process())  ,axis=0)
        #lphwr =  f(fb.process())

        return lphwr


def kaiser_design(fs,width_hz,ripple_db,cutoff_hz):
    # The Nyquist rate of the signal.
    nyq_rate = fs / 2.0
    width = width_hz/nyq_rate
    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)
    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    return taps

if __name__ == '__main__':


    sample_rate = 44100

    sound1 = tone(1*kHz, .1*second)
    sound2 = whitenoise(.1*second)
    sound = sound1+sound2
    sound = sound.ramp()
    samples = np.array(sound)

    transducer = BrianTransducer()

    #s = transducer.get_spikes(samples,sample_rate)
    c = transducer.get_cochleogram(samples,sample_rate)

    plt.imshow(c,aspect='auto')
    plt.show()