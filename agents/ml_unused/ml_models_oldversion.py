import pandas as pd
import numpy as np
from unlzw3 import unlzw
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
import joblib

# decompress data.Z file
with open('connect-4.data.Z', 'rb') as f:
    decompressed = unlzw(f.read())
# save to a normal csv file
with open('connect-4.csv', 'wb') as f:
    f.write(decompressed)

# load into pandas
column_names = [f'cell_{i}' for i in range(42)] + ['outcome'] # 43 rows in data file
data = pd.read_csv('connect-4.csv', names=column_names)
#print(data.head())
#print(data['outcome'].value_counts())

def preprocess_data(df, for_player='x'):
    """
    Preprocess the data before training.
    Parameters
    df: pandas dataframe
    for_player: string x or o to show which player pov to train from

    Returns
    X: np dtype array of board features represented numerically
    y: np dtype array of encoded target labels
    label encoder: labelEncoder object used for decoding predictions
    """
    assert for_player in ['x', 'o'] #player must be either 'x' or 'o'
    df = df.copy()

    # reverse symbols and outcomes if training from o's pov
    if for_player == 'o':
        symbol_map = {'x': 'o', 'o': 'x', 'b': 'b'}
        outcome_map = {'win': 'loss', 'loss': 'win', 'draw': 'draw'}
        for col in df.columns[:-1]:  # exclude outcome col
            df[col] = df[col].map(symbol_map)
        df['outcome'] = df['outcome'].map(outcome_map)

    # convert board symbols to integers: x = 1, o = -1, b = 0
    symbol_to_int = {'x': 1, 'o': -1, 'b': 0}
    for col in df.columns[:-1]:
        df[col] = df[col].map(symbol_to_int)

    # encode outcome labels
    label_encoder = LabelEncoder()
    df['outcome'] = label_encoder.fit_transform(df['outcome']) #

    # feature matrix and target labels
    X = df.iloc[:, :-1].to_numpy().astype(int)
    y = df['outcome'].to_numpy()

    return X, y, label_encoder

# generate training data from both perspectives
X_x, y_x, label_encoder_x = preprocess_data(data, 'x')
X_o, y_o, label_encoder_o = preprocess_data(data, 'o')

# combine them ## why are we combining them
X_combined = np.concatenate((X_x, X_o), axis=0)
y_combined = np.concatenate((y_x, y_o), axis=0)

X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.25, random_state=42) #75% vs 25%

# train Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# train MLP Classifier
mlp_model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=200, random_state=42)
mlp_model.fit(X_train, y_train)

# save models to disk
joblib.dump(rf_model, 'ml_model_rf.joblib')
joblib.dump(mlp_model, 'ml_model_mlp.joblib')

# print evaluation
print("Random Forest Accuracy:", rf_model.score(X_test, y_test))
print("MLP Accuracy:", mlp_model.score(X_test, y_test))