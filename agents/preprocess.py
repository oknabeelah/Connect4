import pandas as pd
import numpy as np
from unlzw3 import unlzw

# load and decompress
with open('connect-4.data.Z', 'rb') as f:
    decompressed = unlzw(f.read())
with open('connect-4.csv', 'wb') as f:
    f.write(decompressed)

"""Acknowledge use of datase: J. Tromp. "Connect-4," UCI Machine Learning Repository, 1995. [Online]. Available: https://doi.org/10.24432/C59P43."""

# load data
column_names = [f'{col}{row}' for row in range(1, 7) for col in 'abcdefg']
column_names.append('outcome')
data = pd.read_csv('connect-4.csv', names=column_names)

# map values to numerical values i.e (x, o, b) = (1, -1, 0)
mapping = {'x': 1, 'o': -1, 'b': 0}
for col in column_names[:-1]: # all except outcome column
    data[col] = data[col].map(mapping)

# map outcome values to numerical values i.e (win, lose, draw) = (1, 0, 0)
outcome_mapping = {'win': 1, 'lose': 0, 'draw': 0} # change to binary data outcome
data['outcome'] = data['outcome'].map(outcome_mapping)

data = data.dropna() # drop rows with missing values

# separate features and labels
X = data.iloc[:, :-1].values
y = data['outcome'].values

# saveeeee
np.save('X.npy', X)
np.save('y.npy', y)

print(f'saved: {X.shape} features, {y.shape} labels')