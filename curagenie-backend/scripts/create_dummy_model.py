#!/usr/bin/env python3
"""
Script to create a dummy ML model for CuraGenie backend testing.
This creates a simple logistic regression model for diabetes risk prediction.
"""

import os
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def create_dummy_model():
    """Create and save a dummy ML model for diabetes risk prediction"""
    
    # Create dummy training data
    # Features: [age, bmi, glucose, blood_pressure, family_history]
    np.random.seed(42)  # For reproducible results
    
    n_samples = 1000
    
    # Generate synthetic data
    age = np.random.normal(45, 15, n_samples)
    bmi = np.random.normal(26, 5, n_samples)
    glucose = np.random.normal(100, 20, n_samples)
    blood_pressure = np.random.normal(120, 15, n_samples)
    family_history = np.random.binomial(1, 0.3, n_samples)  # 30% have family history
    
    X = np.column_stack([age, bmi, glucose, blood_pressure, family_history])
    
    # Create target variable (diabetes risk)
    # Higher risk with: older age, higher BMI, higher glucose, higher BP, family history
    risk_score = (
        (age - 45) * 0.02 +
        (bmi - 26) * 0.1 +
        (glucose - 100) * 0.02 +
        (blood_pressure - 120) * 0.01 +
        family_history * 0.5
    )
    
    # Convert to binary classification (high risk vs low risk)
    y = (risk_score > 0.5).astype(int)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Create and train the model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"Model created successfully!")
    print(f"Training accuracy: {train_accuracy:.3f}")
    print(f"Test accuracy: {test_accuracy:.3f}")
    
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Save the model
    model_path = "models/diabetes_risk_model.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")
    
    # Test prediction
    test_features = [[45, 28.0, 110, 125, 1]]  # High risk example
    prediction = model.predict(test_features)[0]
    probability = model.predict_proba(test_features)[0]
    
    print(f"\nTest prediction:")
    print(f"Features: Age=45, BMI=28.0, Glucose=110, BP=125, Family History=Yes")
    print(f"Prediction: {'High Risk' if prediction else 'Low Risk'}")
    print(f"Probability: {probability}")
    
    return model_path

if __name__ == "__main__":
    create_dummy_model()
