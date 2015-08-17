import os
from abc import ABCMeta, abstractmethod
from scipy.io import wavfile


class Sound(object):
    """
    Abstract class for all modules creating sound_generation
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

        dir_name = 'sound_generation/generated_sounds/'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        wavfile.write(dir_name + str(self), fs, x)
