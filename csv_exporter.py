import csv


class CsvExporter(object):
    """

    """
    @staticmethod
    def export(fname, pitch_extractor, results):
        prediction_file_object = csv.writer(open(fname, 'wb'))

        # Header row
        prediction_file_object.writerow(['Sound', 'Pitch Extractor', 'Pitch Estimate'])

        # Result rows
        for r in results:
            prediction_file_object.writerow([r[0], pitch_extractor, r[1]])
