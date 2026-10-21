import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
import joblib

"""train mlp model to predict best game outcome based on board state (value network) """

# load preprocessed data
X = np.load('X.npy')
y = np.load('y.npy')

# split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# initialise and train mlp
mlp = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=5000, random_state=42)
mlp.fit(X_train, y_train)

# evaluate model
y_pred = mlp.predict(X_test)
print(classification_report(y_test, y_pred))

# save trained model
joblib.dump(mlp, 'value_network.joblib')
print("model saved")
