import numpy as np
from sound import Sound


class PureTone(Sound):
    def __init__(self, f):
        self.f = f

    def generate(self, fs, d):
        t = np.arange(fs * d) / fs
        s = np.sin(2. * np.pi * (self.f) * t)
        return s

    def __str__(self):
        return "Pure_Tone_f_%s.wav" % (self.f)
