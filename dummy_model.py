import numpy as np
from sklearn.dummy import DummyClassifier
import joblib
import os

"""
creates a predictable dummy sklearn model and saves it
as 'agents/dummy_policy_model.joblib' for use in testing the MLAgent
without requiring the fully trained model or mocking libraries.
"""

# define the directory where the agent expects the model
model_dir = "agents"
model_filename = os.path.join(model_dir, "dummy_policy_model.joblib")

# check the directory exists
os.makedirs(model_dir, exist_ok=True)

# create dummy data (needs at least one sample for fit)
X_dummy = np.zeros((1, 42))
# Dummy target variable: make it always predict col 3
y_dummy = np.array([3])

# use DummyClassifier with constant strategy (always predicts 3)

dummy_model = DummyClassifier(strategy="constant", constant=3)
dummy_model.fit(X_dummy, y_dummy)

print(f"Dummy model created. It will always predict: {dummy_model.predict(X_dummy)[0]}")

# save model
try:
    joblib.dump(dummy_model, model_filename)
    print(f"Dummy model saved successfully to: {model_filename}")
except Exception as e:
    print(f"Error saving dummy model: {e}")