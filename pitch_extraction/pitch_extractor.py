from abc import ABCMeta, abstractmethod


class PitchExtractor(object):
    """
    Abstract class for all modules realizing the pitch extraction stage of the human hearing
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract(self, spikes, sample_rate):
        """
        Return a pitch estimate based on the provided neuronal spikes
        :param spikes: Neuronal spikes produced by the cochlea
        :param sample_rate: The sample rate of the audio signal
        :return: The estimated pitch
        """
        pass
