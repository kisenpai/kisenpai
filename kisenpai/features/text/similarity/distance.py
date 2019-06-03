import pandas as pd
import jellyfish


class StringComparison:

    def __init__(self, strings: pd.DataFrame):
        self.strings = strings

    def get_levenshtein_distances(self, to_string: str):
        return self.get_distances(to_string, jellyfish.levenshtein_distance)

    def get_hamming_distances(self, to_string: str):
        return self.get_distances(to_string, jellyfish.hamming_distance)

    def get_jaro_distances(self, to_string: str):
        return self.get_distances(to_string, jellyfish.jaro_distance)

    def get_jaro_winkler_distances(self, to_string: str, tolerance=False):
        distances = pd.DataFrame()
        distances["distance"] = self.strings.apply(
            lambda from_string: jellyfish.jaro_winkler(from_string, to_string, tolerance))
        return distances

    def get_distances(self, to_string: str, distance_function):
        distances = pd.DataFrame()
        distances["distance"] = self.strings.apply(
            lambda from_string: distance_function(from_string, to_string))
        return distances
