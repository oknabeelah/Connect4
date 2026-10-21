import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# move-prediction model

X = np.load("X_progressive.npy") # new dataset
y = np.load("y_progressive.npy") # ""
#X = np.load("X_move_train.npy") # shape is (n, 42)
#y = np.load("y_move_train.npy") # shape is (n, )

current_player = y[:, 1].reshape(-1, 1)
X = np.hstack([X, current_player]) # add current_player to features (43rd)
y = y[:, 0] # ignore current_player as models do not accept multi value labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# train MLP Classifier
mlp_model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=200, random_state=42)
mlp_model.fit(X_train, y_train)

# reshape X for CNN
X_cnn = X[:, :42]  # only the board
X_train_cnn = X_train[:, :42].reshape(-1, 6, 7, 1)
X_test_cnn = X_test[:, :42].reshape(-1, 6, 7, 1)
y_train_cat = to_categorical(y_train, num_classes=7)
y_test_cat = to_categorical(y_test, num_classes=7)

# define CNN
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(6, 7, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, kernel_size=(2, 2), activation='relu', padding='same'),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(7, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# train CNN
model.fit(X_train_cnn, y_train_cat, batch_size=64, epochs=10, verbose=1)

# evaluate
loss, accuracy = model.evaluate(X_test_cnn, y_test_cat, verbose=0)

# save models to disk
joblib.dump(rf_model, 'ml_model_rf.joblib')
joblib.dump(mlp_model, 'ml_model_mlp.joblib')
model.save('cnn_model.h5')

# print evaluation
print("Random Forest Accuracy:", rf_model.score(X_test, y_test))
print("MLP Accuracy:", mlp_model.score(X_test, y_test))
print(f'CNN Accuracy: {accuracy:.4f}')
