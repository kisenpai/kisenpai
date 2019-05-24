import pandas as pd


class DateFeatureExtractor:

    def __init__(self, dates: pd.DataFrame):
        """
        :param dates: The dates should have the format dd.mm.yyyy for example 01.03.1999
        where the "." delimiter can be replaced by any character.
        This class assumes dates contains no missing value.
        """
        self.dates = dates

    def get_features(self) -> pd.DataFrame:
        return self.get_linear_features()

    def get_linear_day(self) -> pd.DataFrame:
        day_feature = pd.DataFrame()
        day_feature["day"] = self.dates.apply(lambda date: date[0:2])
        return day_feature

    def get_linear_month(self) -> pd.DataFrame:
        month_feature = pd.DataFrame()
        month_feature["month"] = self.dates.apply(lambda date: date[3:5])
        return month_feature

    def get_year(self) -> pd.DataFrame:
        year_feature = pd.DataFrame()
        year_feature["year"] = self.dates.apply(lambda date: date[6:10])
        return year_feature

    def get_linear_features(self) -> pd.DataFrame:
        return pd.concat([self.get_linear_day(), self.get_linear_month(), self.get_year()], axis=1, sort=False)
