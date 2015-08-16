import sys
import logging

from pipeline import Pipeline
from transduction.brian_transducer import BrianTransducer
from pitch_extraction.naive_pitch_extractor import NaivePitchExtractor


def main():
    # Read input file path from command line argument
    if len(sys.argv) != 2:
        print 'Please use the application as follows: python main.py <filepath>.wav'
        sys.exit(2)
    fname = sys.argv[1]

    # TODO: Batch processing of sounds
    # TODO: Compare human/model recognition
    # TODO: Maybe save (for instance) spectral images of sounds that failed

    # Setup logging
    logging.basicConfig(filename='pitch_perception.log', level=logging.INFO)

    # Set dependencies
    transducer = BrianTransducer()
    pitch_extractor = NaivePitchExtractor()

    # Init pipeline
    pipeline = Pipeline(transducer, pitch_extractor, test_mode=False)

    # Run processing
    pitch = pipeline.process(fname)

    log_string = 'File: %s\tPitch: %i' % (fname, pitch)
    logging.info(log_string)

    # Output final pitch
    print pitch

if __name__ == "__main__":
    main()
