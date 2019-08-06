# kisenpai

This library is intended to ease the process of feature engineering. Most tasks like feature extraction, selection and transformation are usually done over and over again across projects. Not only this creates duplicate code, but it is also time consuming to recopy those useful functions over and over again. With **kisenpai**, you now have a central library that handles diverse feature engineering tasks.

## Installation
```shell
pip install kisenpai
```
Not all features are currently released on pypi. To use the latest features, clone the project.

## Features
Kisenpai is essentially a wrapper for many useful common functions. (Note that the constructors always take a dataframe as input). Here are some of the features:

### Usecase Features

#### Date - Feature Extraction
1. Extract all date features from date string
```python
from features.usecase.date.date import DateFeatureExtractor
import pandas as pd

column_name = "date"
df = pd.DataFrame(["The 1st of June 1994", "2nd June 2000"], columns=[column_name])
dfe = DateFeatureExtractor(df, column_name, day_first=False, fuzzy_with_tokens=True)
features = dfe.get_features()
print(features.head())
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
3. Extract features from date string (German like format - with day first %d.%m.%Y)
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

### Text Features

#### Spelling Correction - Feature Transformation
We use pyspellcheker for spelling corrections. It supports English, Spanish, German, French, and Portuguese.
1. Auto correction of french text
```python
column_name = "text"
df = pd.DataFrame(["bonjor", "mersi"], columns=[column_name])

dfe = SpellingCorrector(df, column_name, language="fr")
features = dfe.get_correct_spellings()
```
```shell
      text
0  bonjour
1    merci
```
2. Auto correction of english text.
```python
df = pd.DataFrame(["good mornin my namme is Kisenpai", "I em goud enough"], columns=[column_name])

dfe = SpellingCorrector(df, column_name, language="en", distance=1)
features = dfe.get_correct_spellings()
```
```shell
                               text
0  good morning my name is Kisenpai
1                  I em good enough
```
#### String Comparison - Feature Extraction
Get the distances (hamming, levenstein, jaro and jaro-winkler) from one string to all other string in the dataframe column. We use the jellyfish library
```python
column_name = "text"
df = pd.DataFrame(["word", "wordy"], columns=[column_name])

dfe = StringComparison(df, column_name)
features = dfe.get_jaro_distances("wardy")
```
```shell
   distance
0  0.783333
1  0.866667
```

## Feature Selection
#### With Genetic Algorithms
We implemented feature selection with a genetic algorithm. Our implmentation is a tweaked version of DEAP's (A python library for evolutionary systems) solution for the One-Max (all-ones) problem. Here is how you can use Kisenpai's feature selector.
```python
# 1. Import required libraries
import pandas as pd
from kisenpai.features.selector.feature_selector import FeatureSelector

# 2. Load your data and seperate the features from the labels or targets
data = pd.read_csv("data.csv", encoding="utf-8", delimiter=",")
labels = data["Target"]
data.drop(columns=["Target], inplace=True)

# 3. Define the training function
def train_evaluate(selected_features) -> float:
  # see comments below
  return some_metric

print(data.head())
fs = FeatureSelector(data, train_evaluate)
features = fs.get_selected_features()
print(features.head())
```
Now about the **train_evaluate(selected_features) -> float** function.
- The feature selector finds the best features by training a different models based on different features.
- It then evolves towards the best features, hence the best model.
- For this to work, we need the **train_evaluate(selected_features) -> float** function.
- This should be your training-evaluation function. It takes as input the features sent by the feature selector and returns an evaluation metric (For example, accuracy, F1-score, recall etc.).
- The objective is to maximise this metric. Hence, the current version will not work for metrics that have to be minimised e.g loss metrics.
- Don't forget to set your random state before training. This is required for the evolution to work properly.
- Below is an example of such a function. We train, our model based on the features received, and return the accuracy.

```python
# Import required libraries
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import numpy as np

def train_evaluate(selected_features: list) -> float:
    subset_data = data[selected_features]
    X_train, X_valid, y_train, y_valid = train_test_split(subset_data, labels, test_size=0.20, random_state=42)
    classifier = GaussianNB().fit(X_train, y_train)
    labels_predicted = classifier.predict(X_valid)
    return np.mean(labels_predicted == y_valid)
```
This function was intitally passed to the FeatureSelector's constructor. The **get_selected_features()** returns a new dataset with selected columns (features) only.

Here is a screenshot of one of the experiments we conducted with only 100 generation. You can see how the accuracy increases generation. It seems like it is stuck in a local-optima, but during previous tests, we reached 0.85 accuracy with 300 generations.


![alt text](https://github.com/kisenpai/kisenpai/blob/feature-selector/kisenpai/features/selector/Screenshot%202019-08-06%20at%2022.30.48.png "Performance Evolution")
