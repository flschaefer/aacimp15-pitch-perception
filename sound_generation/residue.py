import numpy as np
from sound import Sound


class Residue(Sound):
    def __init__(self, n, df, m, g):
        self.n = n
        self.df = df
        self.m = m
        self.g = g

    def generate(self, fs, d):
        t = np.arange(fs * d) / fs
        s = 0.5 * self.m * np.sin(2. * np.pi * ((self.n - 1) * self.g + self.df) * t) + \
            np.sin(2. * np.pi * (self.n * self.g + self.df) * t) + \
            0.5 * self.m * np.sin(2. * np.pi * ((self.n + 1) * self.g + self.df) * t)
        return s

    def __str__(self):
        return "Residue_g_%s_m_%s_df_%s_n_%s.wav" % (self.g, self.m, self.df, self.n)


def residue(d=0.2, n=10, df=50., fs=44100., m=0.9, g=200.):
    """
    Creates sound_generation as described in Schouten's residue pitch
    Input
    - d: duration (s)
    - n: central harmonic of the triplet
    - df: shift (Hz)
    - g: fundamental frequency
    - fs: sampling frequency
    - m: gain (1+m*cos)*sin
    Output
    - Waveform of sound
    """
    t = np.arange(fs * d) / fs
    s = 0.5 * m * np.sin(2. * np.pi * ((n - 1) * g + df) * t) + \
        np.sin(2. * np.pi * (n * g + df) * t) + \
        0.5 * m * np.sin(2. * np.pi * ((n + 1) * g + df) * t)
    return s
