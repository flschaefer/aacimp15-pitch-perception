import numpy as np
from scipy.signal import butter, lfilter
from sound import Sound


class Harmonics(Sound):
    def __init__(self, f0, typ, region):
        assert isinstance(f0, float)
        assert typ in ["SIN", "ALT"]
        assert region in ["LOW", "MID", "HIGH"]

        self.f0 = f0
        self.typ = typ
        self.region = region

    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def generate(self, fs, d):

        t = np.arange(d * fs) / fs
        regions = {"LOW": [125., 625.],
                   "MID": [1375., 1875.],
                   "HIGH": [3900., 5400.]}
        region = regions[self.region]

        k = 100
        phi = np.zeros((k,))
        if self.typ == "ALT":
            phi[::2] = np.pi / 2

        s = np.zeros((len(t),))
        for i in range(k):
            s += np.cos(2. * np.pi * self.f0 * (i + 1) * t + phi[i])

        sf = self.butter_bandpass_filter(s, region[0], region[1], fs, order=4)
        return sf

    def __str__(self):
        return "Harmonics_f0_%s_type_%s_region_%s.wav" % (self.f0, self.typ, self.region)


