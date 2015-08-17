from matplotlib import pyplot as plt
import numpy as np
from scipy.io import wavfile
import glob

def plot_and_save_sound(fname):

    name = fname.split('/')[-1]
    sound = wavfile.read(fname)
    samples, fs = sound[1], sound[0]
    n = len(samples)
    t = np.arange(n)/float(fs)

    freqs = np.fft.fftfreq(n)*fs
    s = np.abs(np.fft.fft(samples))
    fmax = 10000.
    ind = (freqs>0)&(freqs<fmax)

    fig,axarr = plt.subplots(2,1)
    d = 0.05
    n_plot = int(d*fs)
    axarr[0].plot(t[:n_plot],samples[:n_plot])
    axarr[0].set_xlabel('time (ms)')
    axarr[0].set_title(name)


    axarr[1].plot(freqs[ind],s[ind])
    axarr[1].set_xlabel('freq (Hz)')

    fig.savefig(fname.split('.wav')[0]+'.png')


if __name__ == '__main__':
    path = '/home/vincent/git/aacimp15-pitch-perception/sounds/'
    files = glob.glob(path+'*.wav')
    for f in files:
        print f
        plot_and_save_sound(f)