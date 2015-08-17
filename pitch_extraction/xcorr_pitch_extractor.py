import numpy as np
from brian import *
from brian.hears import *
from matplotlib import pyplot as plt

class XcorrPitchExtractor(object):
    """
    Fast Autocorrelation Extractor
    """

    def __init__(self, n_channels=3000.):
        self.n_channels = n_channels
        """
        Empty constructor. Fill with code if needed
        """
        pass

    def extract(self, spikes, sample_rate):
        t,nc = spikes.shape
        assert nc == self.n_channels

        # Autocorrelation across all channels
        corr= np.zeros((2*t-1,))
        dt = 1./sample_rate
        for r in spikes.T:
            corr += np.correlate(r, r, mode='full')
        corr = corr[corr.size/2:]
        corr = corr/(np.arange(0,len(corr))*dt)
        plt.plot(corr)
        plt.show()
        ts,vs = get_peaks(corr,sample_rate)
        imax = np.argmax(vs)
        return 1./ts[imax]



def get_peaks(x,fs):
    g = np.diff(x)
    i = np.zeros((len(x)-1,))
    i[1:] = (g[1:]<0)*(g[:-1]>0)
    ind = np.where(i)[0]
    taus = ind/float(fs)
    values = x[ind]
    return taus,values



if __name__ == '__main__':

    N_channels = 300
    sample_rate= 44100.
    spikes = np.random.randn(N_channels,1000)
    pe = XcorrPitchExtractor(N_channels)
    pitch = pe.extract(spikes.T, sample_rate)
    print pitch