import numpy as np
from scipy.io import wavfile

from tests.transducer_test import TransducerTest
from tests.pitch_extractor_test import PitchExtractorTest


class Pipeline(object):
    """
    Pipeline class that combines all simulated stages of human pitch perception
    """

    def __init__(self, transducer, pitch_extractor, test_mode=False):
        """
        :param transducer: The module used for the transduction stage
        :param pitch_extractor: The module used for the pitch extraction stage
        :param test_mode:
        """
        self.transducer = transducer
        if test_mode:
            TransducerTest.run_tests(self.transducer)

        self.pitch_extractor = pitch_extractor
        if test_mode:
            PitchExtractorTest.run_tests(self.pitch_extractor)

    def check_input_format(self, sound):
        """
        Check if input has the correct format
        :param sound: Sound input to be checked
        """
        assert type(sound) is tuple
        assert len(sound) == 2
        assert type(sound[0] is int), 'Sample rate has to be an integer'
        assert type(sound[1]) is np.ndarray, 'Sound samples have to be a numpy array!'

    def process(self, fname):
        """
        Processes the input sound file using to Pipeline to retrieve the appropriate pitch
        :param fname: File path of the input sound file
        :return: The retrieved pitch
        """
        # Load sound and check if it has the correct format
        sound = wavfile.read(fname)
        self.check_input_format(sound)

        samples, sample_rate = sound[1], sound[0]

        spikes = self.transducer.get_spikes(samples, sample_rate)

        pitch = self.pitch_extractor.extract(spikes, sample_rate)

        return pitch
