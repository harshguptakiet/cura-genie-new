#!/usr/bin/env python3
"""
Training script for Diabetes and Alzheimer's models
using structured CSV data.
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load Diabetes Data
print("Loading Diabetes Data...")
diabetes_data = pd.read_csv(r'C:\Users\xhgme\curagenie-frontend\ml model data\diabetes\diabetes.csv')
X_diabetes = diabetes_data.drop('Outcome', axis=1)
y_diabetes = diabetes_data['Outcome']

# Preprocess
scaler = StandardScaler()
X_diabetes = scaler.fit_transform(X_diabetes)

# Split
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_diabetes, y_diabetes, test_size=0.2, random_state=42)

# Train Model
print("Training Diabetes Model...")
diabetes_model = LogisticRegression()
diabetes_model.fit(X_train_d, y_train_d)

# Evaluate
y_pred_d = diabetes_model.predict(X_test_d)
print(f"Diabetes Accuracy: {accuracy_score(y_test_d, y_pred_d):.2f}")

# Save Model
with open('models/diabetes_model.pkl', 'wb') as f:
    pickle.dump(diabetes_model, f)
print("Diabetes model saved.")

# Load Alzheimer's Data
print("Loading Alzheimer's Data...")
alz_data = pd.read_csv(r'C:\Users\xhgme\curagenie-frontend\ml model data\alzhiemer\alzheimers_disease_data.csv')
X_alz = alz_data.drop(['Diagnosis', 'PatientID', 'DoctorInCharge'], axis=1)  # Drop irrelevant columns
y_alz = alz_data['Diagnosis']

# Preprocess
X_alz = scaler.fit_transform(X_alz)

# Split
X_train_a, X_test_a, y_train_a, y_test_a = train_test_split(X_alz, y_alz, test_size=0.2, random_state=42)

# Train Model
print("Training Alzheimer's Model...")
alz_model = LogisticRegression()
alz_model.fit(X_train_a, y_train_a)

# Evaluate
y_pred_a = alz_model.predict(X_test_a)
print(f"Alzheimer's Accuracy: {accuracy_score(y_test_a, y_pred_a):.2f}")

# Save Model
with open('models/alzheimer_model.pkl', 'wb') as f:
    pickle.dump(alz_model, f)
print("Alzheimer's model saved.")


