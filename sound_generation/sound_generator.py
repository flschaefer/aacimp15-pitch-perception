import numpy as np

from harmonics import Harmonics
from residue import Residue
from pure_tone import PureTone


class SoundGenerator(object):
    def __init__(self, sample_rate):
        self.fs = sample_rate

    def generate_harmonic_sounds(self):
        d = 0.2
        f0s = [62.5, 125., 250.]
        regions = ["LOW", "MID", "HIGH"]
        conditions = ["ALT", "SIN"]

        for f0 in f0s:
            for typ in conditions:
                for region in regions:
                    print f0, typ, region

                    sound = Harmonics(f0, typ, region)
                    print str(sound)
                    sound.save_to_wav(self.fs, d)

    def generate_residue_sounds(self):
        # settings for the residue
        d = 0.2
        df = 50.
        g = 200.
        m = 0.9
        ns = [9, 10, 11]
        dfs = np.arange(-6 + 1, 6) * df

        for n in ns:
            for df in dfs:
                sound = Residue(n, df, m, g)
                print str(sound)
                sound.save_to_wav(self.fs, d)

    def generate_pure_sound(self):
        d = 0.2
        fs = 44100.
        f = 1000.

        sound = PureTone(f)
        sound.save_to_wav(fs, d)

    def generate_sounds(self):
        self.generate_harmonic_sounds()
        self.generate_residue_sounds()


def main():
    # TODO: Maybe select path where to save sound_generation
    sound_generator = SoundGenerator(44100.)
    sound_generator.generate_sounds()


if __name__ == "__main__":
    main()
