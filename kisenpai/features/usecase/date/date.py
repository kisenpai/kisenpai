import pandas as pd
from dateutil import parser


class DateFeatureExtractor:

    def __init__(self, data: pd.DataFrame, column_name: str, day_first=False, fuzzy_with_tokens=False):
        self.dates = data[column_name]
        self.dates = self.dates.apply(lambda date: self.__parse_date(date, day_first, fuzzy_with_tokens))

    def __parse_date(self, date: str, day_first=False, fuzzy_with_tokens=False) -> str:
        datetime = parser.parse(date, dayfirst=day_first, fuzzy_with_tokens=fuzzy_with_tokens)
        if fuzzy_with_tokens:
            return datetime[0].strftime("%d.%m.%Y")
        return datetime.strftime("%d.%m.%Y")

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


d = DateFeatureExtractor(pd.DataFrame(["The 1st June 2009", "3rd of April 1999"], columns=["date"]), "date", True, True)
print(d.dates)
