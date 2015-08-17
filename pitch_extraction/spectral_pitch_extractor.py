from brian import *
from brian.hears import *


class SpectralPitchExtractor(object):
    """
    A computational model of the human's hearing pitch extraction stage, using the spacial model
    """

    def __init__(self):
        """
        Empty constructor. Fill with code if needed
        """
        pass

    def extract(self, spikes, sample_rate):
        Nf = 300
        # Channel frequinces are unnessesary as well as Nf
        cf = erbspace(20 * Hz, 20 * kHz, Nf)
        # TODO: Compute excitatory pattern (for each auditory nerve, sum up along the time dimension)
        sa = np.sum(spikes, axis=0)
        log_sa = np.log2(sa)

        # TODO: Use a pitch estimation method like pattern Matching, wightman, goldstein, Terhardt,...

        # I used Terhardt's virtual pitch
        peaks_lst = self.peaks(sa, cf, Nf)
        N = peaks_lst.size

        w = 1.
        index_score = np.zeros(N)
        H = 0

        for i in range(N):
            for j in range(N):
                if peaks_lst[j] != 0:
                    H += w / (j + 1.) * (peaks_lst[i] + np.log2(j + 1))
            index_score[i] = H
            H = 0

        # TODO: Return pitch estimate
        return cf[index_score.tolist().index(max(index_score))]

    # Function for extraction peaks in spikes activity
    def peaks(self, spikes_sum, cf, Nf=3000):
        e = spikes_sum / np.max(spikes_sum)
        l = int(100 * Nf / 3000.)
        w = np.exp(-((np.arange(l) - l / 2) / float(l)) ** 2 * 20.)

        e = np.convolve(e, w, mode='same')
        peaks = np.zeros(e.shape)
        grad = np.diff(e)

        v = np.zeros((len(e),))
        v[:len(e) - 2] = ((np.sign(grad[0:-1]) > 0) * (np.sign(grad[1:]) < 0)) * (np.abs(grad[0:-1] * grad[1:]))
        v = v / np.max(v)
        r = np.zeros(v.shape)
        j = 0
        for i in v:
            if i > 0:
                r[j] = cf[i]
            j += 1

        return r
