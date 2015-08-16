import sys
import glob
import logging

from pipeline import Pipeline
from transduction.brian_transducer import BrianTransducer
from pitch_extraction.naive_pitch_extractor import NaivePitchExtractor


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
    pitch_extractor = NaivePitchExtractor()

    # Init pipeline
    pipeline = Pipeline(transducer, pitch_extractor, test_mode=False)

    for af in audio_files:
        # Run processing
        pitch = pipeline.process(af)

        log_string = 'File: %s\tPitch: %i' % (af, pitch)
        logging.info(log_string)

        # Output final pitch
        print log_string

if __name__ == "__main__":
    main()
