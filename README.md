# kisenpai

This library is intended to ease the process of feature engineering. Most tasks like feature extraction, selection and transformation are usually done over and over again across projects. Not only this creates duplicate code, but it is also time consuming to recopy those useful functions over and over again. With **kisenpai**, you now have a central library that handles diverse feature engineering tasks.

## Features
Kisenpai is essentially a wrapper for many useful common functions. (Note that the constructors always take a dataframe as input). Here are some of the features:

#### Date Feature Extraction
1. Extract all date features from date string
```python
from features.usecase.date.date import DateFeatureExtractor
import pandas as pd

column_name = "date"
df = pd.DataFrame(["The 1st of June 1994", "2nd June 2000"], columns=[column_name])
dfe = DateFeatureExtractor(df, column_name, day_first=False, fuzzy_with_tokens=True)
features = dfe.get_features()
``` 
```shell
  day month  year
0  01    06  1994
1  02    06  2000
```
2. Extract the month from date string
```python
df = pd.DataFrame(["1994-03-14", "1995-04-15"], columns=[column_name])
dfe = DateFeatureExtractor(df, column_name, day_first=False, fuzzy_with_tokens=False)
features = dfe.get_linear_month()
```
```shell
  month
0    03
1    04
```
3. Extract features from date string (German like format - with day first)
```python
df = pd.DataFrame(["18.08.2004", "23.12.2019"], columns=[column_name])
dfe = DateFeatureExtractor(df, column_name, day_first=True, fuzzy_with_tokens=False)
features = dfe.get_features()
```
```shell
  day month  year
0  18    08  2004
1  23    12  2019
```
