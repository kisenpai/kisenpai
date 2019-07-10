# kisenpai

This library is intended to ease the process of feature engineering. Most tasks like feature extraction, selection and transformation are usually done over and over again across projects. Not only this creates duplicate code, but it is also time consuming to recopy those useful functions over and over again. With **kisenpai**, you now have a central library that handles diverse feature engineering tasks.

## Features
Kisenpai is essentially a wrapper for many useful common functions. Here are some of them:

#### Date Feature Extraction
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
