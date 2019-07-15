import pandas as pd
from spellchecker import SpellChecker


class SpellingCorrector:

    def __init__(self, data: pd.DataFrame, column_name: str, language: str, local_dictionary=None, distance=2):
        self.__strings = data[column_name]
        self.__spell_checker = SpellChecker(language=language, local_dictionary=local_dictionary, distance=distance)

    def get_correct_spellings(self):
        return pd.DataFrame(self.__strings.apply(lambda text: self.__auto_correct_text(text)))

    def __auto_correct_text(self, text: str):
        corrected_text = ""
        accumulator = ""
        for char in text:
            if char.isalpha():
                accumulator += char
            else:
                if len(accumulator) > 0:
                    accumulator = self.__spell_checker.correction(accumulator)
                accumulator += char
                corrected_text += accumulator
                accumulator = ""
        corrected_text += self.__spell_checker.correction(accumulator)
        return corrected_text
