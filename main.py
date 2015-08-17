import sys
import glob
import logging

from pipeline import Pipeline
from transduction.brian_transducer import BrianTransducer
from pitch_extraction.naive_pitch_extractor import NaivePitchExtractor
from pitch_extraction.temporal_pitch_extractor import TemporalPitchExtractor
from pitch_extraction.spectral_pitch_extractor import SpectralPitchExtractor
from csv_exporter import CsvExporter
from config import Config


def main():
    # Read input file path from command line argument
    if len(sys.argv) != 2:
        print 'Please use the application as follows: python main.py <filepath>.wav'
        sys.exit(2)
    fpath = sys.argv[1]

    # If the file path ends with .wav only the given file will be processed
    # Else we assume that the input is a path to all the .wav files to be batch processed
    audio_files = []
    if fpath.endswith('.wav'):
        audio_files.append(fpath)
    else:
        audio_files.extend(glob.glob(fpath + '/*.wav'))

    # TODO: Compare human/model recognition
    # TODO: Maybe save (for instance) spectral images of sounds that failed

    # Setup logging
    logging.basicConfig(filename='pitch_perception.log', level=logging.INFO)

    # Set dependencies
    transducer = BrianTransducer()
    available_pitch_extractors = {'naive': NaivePitchExtractor, 'spectral': SpectralPitchExtractor(),
                                  'temporal': TemporalPitchExtractor}
    pitch_extractor = available_pitch_extractors[Config.get_config_option('pitch_extraction')]

    # Init pipeline
    pipeline = Pipeline(transducer, pitch_extractor, test_mode=False)

    # Collect results
    results = []

    for af in audio_files:
        # Run processing
        pitch = pipeline.process(af)

        log_string = 'File: %s\tPitch: %i' % (af, pitch)
        logging.info(log_string)

        # Output final pitch
        print log_string

        results.append((af, pitch))

    # Export results
    CsvExporter.export('results.csv', pitch_extractor.__class__.__name__, results)


if __name__ == "__main__":
    main()
