from abc import ABCMeta, abstractmethod
from scipy.io.wavfile import write

class SoundGeneration(object):
    """
    Abstract class for all modules creating sounds
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate(self, fs, d):
        """
        Return the waveform as an array
        :param fs: The sample rate of the audio signal
        :return: The estimated pitch
        """
        pass



    def save_to_wav(self, fs, d):
        """
        Return the waveform as an array
        :param fs: The sample rate of the audio signal
        :return: The estimated pitch
        """
        x = self.generate(fs, d)
        write(str(self),fs,x)