from abc import ABCMeta, abstractmethod


class Transducer(object):
    """
    Abstract class for all modules realizing the transduction stage of the human hearing
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_spikes(self, samples, sample_rate):
        """
        Computes the neuronal spikes produced by the human cochlea
        :param samples: An array of audio samples
        :param sample_rate: The sample rate of the audio signal
        :return: An array of neuronal spikes
        """
        pass
