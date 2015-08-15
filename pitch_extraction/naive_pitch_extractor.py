import numpy as np
from brian import *
from brian.hears import *

from pitch_extractor import PitchExtractor


class NaivePitchExtractor(PitchExtractor):
    """
    A very naive pitch extractor implementation, just for testing
    """

    def extract(self, spikes, sample_rate):
        cf = erbspace(20*Hz, 20*kHz, 300)

        b = np.sum(spikes, axis=0)

        # Maximum ?
        m = np.max(b)

        # Frequency?
        idx = list(b).index(m)
        return cf[idx]
