import pickle
import os
from sklearn.linear_model import LogisticRegression
import numpy as np

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Create and train a simple diabetes risk prediction model
# Features: [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
np.random.seed(42)  # For reproducibility

# Generate synthetic training data
n_samples = 1000
X = np.random.rand(n_samples, 8)
X[:, 0] = np.random.randint(0, 18, n_samples)      # Pregnancies: 0-17
X[:, 1] = X[:, 1] * 150 + 50                       # Glucose: 50-200
X[:, 2] = X[:, 2] * 80 + 40                        # BloodPressure: 40-120
X[:, 3] = X[:, 3] * 80 + 20                        # SkinThickness: 20-100
X[:, 4] = X[:, 4] * 400                            # Insulin: 0-400
X[:, 5] = X[:, 5] * 30 + 18                        # BMI: 18-48
X[:, 6] = X[:, 6] * 2                                # DiabetesPedigreeFunction: 0-2
X[:, 7] = X[:, 7] * 60 + 21                        # Age: 21-81

# Create target variable (diabetes risk)
y = (
    (X[:, 0] > 6) * 0.1 +        # Pregnancies
    (X[:, 1] > 140) * 0.3 +      # Glucose
    (X[:, 2] > 90) * 0.1 +       # BloodPressure
    (X[:, 4] > 200) * 0.1 +      # Insulin
    (X[:, 5] > 30) * 0.2 +       # BMI
    (X[:, 6] > 1) * 0.1 +        # Pedigree
    (X[:, 7] > 45) * 0.1 +       # Age
    np.random.rand(n_samples) * 0.1  # Random noise
) > 0.5

# Train the model
model = LogisticRegression(random_state=42)
model.fit(X, y)

# Save the model
with open('models/diabetes_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ ML model created and saved to models/diabetes_model.pkl")
print(f"Model accuracy on training data: {model.score(X, y):.3f}")

# Test the model with sample data
test_data = [
    [2, 120, 70, 20, 80, 25.0, 0.4, 30],   # Low risk profile
    [8, 180, 90, 40, 200, 35.0, 0.8, 55],  # High risk profile
]

for i, data in enumerate(test_data):
    prediction = model.predict([data])[0]
    probability = model.predict_proba([data])[0]
    print(f"Test case {i+1}: {'High Risk' if prediction else 'Low Risk'} (confidence: {max(probability):.3f})")
