# ML Model Replacement Guide for CuraGenie

## Current Dummy Model Analysis

**Location:** `models/diabetes_risk_model.pkl`  
**Type:** Logistic Regression trained on synthetic data  
**Accuracy:** 98.5% (artificially high due to fake data)  
**Purpose:** Testing and demonstration only

## Requirements for Real ML Model

### 1. Technical Interface Requirements

Your replacement model MUST implement these exact methods:

```python
# Required methods (used in worker/tasks.py)
prediction = model.predict([features])[0]           # Returns: 0 or 1
prediction_proba = model.predict_proba([features])[0]  # Returns: [prob_0, prob_1]

# Example usage in your model:
class YourRealModel:
    def predict(self, X):
        # Must return array of 0s and 1s
        return np.array([0 or 1])
    
    def predict_proba(self, X):
        # Must return array of [low_risk_prob, high_risk_prob]
        return np.array([[0.3, 0.7]])  # Example: 30% low risk, 70% high risk
```

### 2. Input Feature Requirements

**Exact feature order and types:**
```python
features = [
    age,              # float: 18-100 years
    bmi,              # float: 15-50 BMI
    glucose_level,    # float: 70-300 mg/dL
    blood_pressure,   # float: 90-200 mmHg systolic
    family_history    # int: 0 (no) or 1 (yes)
]

# Example valid input:
[45.5, 28.2, 125.0, 140.0, 1]  # 45yo, BMI 28.2, glucose 125, BP 140, family history
```

### 3. Model Storage Requirements

```python
# File location (hardcoded in worker/tasks.py line 34)
model_path = "models/diabetes_model.pkl"

# Saving your model:
import pickle
with open('models/diabetes_model.pkl', 'wb') as f:
    pickle.dump(your_trained_model, f)

# Must be compatible with this loading code:
with open('models/diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)  # Your model must work here
```

## Data Requirements for Real Model

### Minimum Dataset Specifications

| Requirement | Minimum | Recommended | Production |
|-------------|---------|-------------|------------|
| **Patients** | 10,000 | 50,000 | 100,000+ |
| **Follow-up time** | 2 years | 5 years | 10 years |
| **Diabetes cases** | 1,000 | 5,000 | 10,000+ |
| **Demographics** | Single site | Multi-site | Multi-country |

### Required Data Sources

#### Option 1: Clinical Trial Data
```
- Randomized controlled trials
- Prospective cohort studies  
- Multi-center studies
- Long-term follow-up data
```

#### Option 2: Electronic Health Records
```
- Hospital EHR systems
- Primary care databases
- Insurance claims data
- Laboratory results
```

#### Option 3: Public Health Datasets
```
- NHANES (National Health and Nutrition Examination Survey)
- UK Biobank
- Framingham Heart Study
- ARIC (Atherosclerosis Risk in Communities)
```

### Data Processing Requirements

```python
# Example data preprocessing pipeline
def preprocess_medical_data(raw_data):
    processed = {}
    
    # Age normalization
    processed['age'] = np.clip(raw_data['age'], 18, 100)
    
    # BMI calculation and validation
    processed['bmi'] = np.clip(raw_data['weight'] / (raw_data['height']**2), 15, 50)
    
    # Glucose level standardization
    processed['glucose_level'] = np.clip(raw_data['fasting_glucose'], 70, 300)
    
    # Blood pressure validation
    processed['blood_pressure'] = np.clip(raw_data['systolic_bp'], 90, 200)
    
    # Family history encoding
    processed['family_history'] = 1 if raw_data['family_diabetes'] else 0
    
    return [processed['age'], processed['bmi'], processed['glucose_level'], 
            processed['blood_pressure'], processed['family_history']]
```

## Model Performance Requirements

### Clinical Performance Metrics

```python
# Minimum acceptable metrics for diabetes risk prediction
required_metrics = {
    "sensitivity": 0.80,    # 80% of high-risk patients correctly identified
    "specificity": 0.75,    # 75% of low-risk patients correctly identified  
    "auc_roc": 0.85,        # Area under ROC curve ≥ 0.85
    "precision": 0.70,      # 70% of high-risk predictions are correct
    "recall": 0.80,         # 80% of actual high-risk cases are caught
    "f1_score": 0.75,       # Balanced precision and recall
}

# Validation requirements
validation_requirements = {
    "cross_validation": "5-fold minimum",
    "external_validation": "Independent dataset required",
    "temporal_validation": "Test on future time periods",
    "demographic_validation": "Test across age, gender, ethnicity"
}
```

### Model Interpretability

```python
# Your model should support explanation methods
class InterpretableModel:
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def get_feature_importance(self):
        # Return importance of each feature
        return {
            'age': 0.25,
            'bmi': 0.20, 
            'glucose_level': 0.35,
            'blood_pressure': 0.15,
            'family_history': 0.05
        }
    
    def explain_prediction(self, features):
        # Explain why a specific prediction was made
        return "High risk due to elevated glucose (125 mg/dL > 100 threshold)"
```

## Regulatory and Compliance Requirements

### Data Privacy Requirements

```python
# All training data must be de-identified
required_removals = [
    "patient_name", "ssn", "phone", "email", "address",
    "medical_record_number", "account_number", "license_number",
    "biometric_identifiers", "facial_photos", "fingerprints"
]

# Dates must be shifted consistently
def de_identify_dates(patient_data):
    # Shift all dates by random offset for each patient
    offset = random.randint(-365, 365)  # ±1 year
    patient_data['diagnosis_date'] += timedelta(days=offset)
    return patient_data
```

### HIPAA Compliance Checklist

- [ ] Business Associate Agreement with data providers
- [ ] Data encryption in transit and at rest
- [ ] Access controls and audit logging
- [ ] Staff training on HIPAA requirements
- [ ] Incident response procedures
- [ ] Regular security assessments

### FDA Medical Device Considerations

If your model will be used for clinical diagnosis:

- [ ] FDA 510(k) premarket notification
- [ ] Clinical validation studies
- [ ] Quality management system (ISO 13485)
- [ ] Risk management documentation
- [ ] Post-market surveillance plan

## Implementation Steps

### Step 1: Data Acquisition (3-6 months)
```bash
# Institutional partnerships
- Partner with hospitals/clinics
- Obtain IRB approval
- Sign data use agreements
- Implement de-identification pipeline
```

### Step 2: Model Development (2-4 months)
```python
# Development pipeline
1. Exploratory data analysis
2. Feature engineering and selection
3. Model training and hyperparameter tuning
4. Cross-validation and performance evaluation
5. Bias testing across demographics
```

### Step 3: Clinical Validation (6-12 months)
```bash
# Validation requirements
- External validation dataset
- Prospective clinical study
- Physician review of predictions
- Patient outcome tracking
```

### Step 4: Deployment Preparation (1-2 months)
```python
# Replace dummy model
def deploy_real_model():
    # 1. Save trained model
    with open('models/diabetes_model.pkl', 'wb') as f:
        pickle.dump(trained_real_model, f)
    
    # 2. Update model loading (no code changes needed)
    # 3. Test with real clinical data
    # 4. Monitor performance in production
```

## Alternative: Intermediate Approaches

### Option 1: Use Pre-trained Model
```python
# Use existing validated diabetes risk models
# Example: American Diabetes Association Risk Calculator
# Implement their algorithm with your interface

def ada_risk_calculator(age, bmi, glucose, bp, family_history):
    # Implement published ADA risk formula
    risk_score = calculate_ada_score(age, bmi, glucose, bp, family_history)
    return 1 if risk_score > threshold else 0
```

### Option 2: Synthetic but Realistic Data
```python
# Generate more realistic synthetic data based on medical literature
def generate_realistic_synthetic_data(n_samples=50000):
    # Use published diabetes risk factors and distributions
    # Based on epidemiological studies
    # More realistic than current random data
    pass
```

### Option 3: Transfer Learning
```python
# Start with pre-trained model and fine-tune on your data
def transfer_learning_approach():
    # Use model trained on similar medical prediction task
    # Fine-tune on diabetes-specific data
    # Requires less data than training from scratch
    pass
```

## Testing Your Replacement Model

```python
# Test script to validate your new model
def test_new_model():
    import pickle
    
    # Load your model
    with open('models/diabetes_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Test required interface
    test_features = [[45, 28.0, 110, 120, 0]]
    
    # Test prediction method
    prediction = model.predict(test_features)[0]
    assert prediction in [0, 1], "Prediction must be 0 or 1"
    
    # Test probability method
    proba = model.predict_proba(test_features)[0]
    assert len(proba) == 2, "Must return probability for both classes"
    assert abs(sum(proba) - 1.0) < 0.001, "Probabilities must sum to 1"
    
    print("✅ Model interface tests passed!")
    print(f"Prediction: {'High Risk' if prediction else 'Low Risk'}")
    print(f"Confidence: {max(proba):.3f}")

# Run this test before deploying
test_new_model()
```

## Budget and Timeline Estimates

### Budget Requirements

| Component | Cost Range | Notes |
|-----------|------------|-------|
| **Data Acquisition** | $50K - $500K | Hospital partnerships, IRB fees |
| **Data Scientists** | $200K - $400K | 2-3 scientists for 6-12 months |
| **Clinical Consultants** | $50K - $200K | Medical oversight |
| **Regulatory Consulting** | $100K - $300K | FDA/HIPAA compliance |
| **Validation Studies** | $200K - $1M | Clinical trials |
| **Total** | $600K - $2.4M | Full clinical-grade model |

### Timeline Estimates

| Phase | Duration | Parallel Activities |
|-------|----------|-------------------|
| **Data Acquisition** | 3-6 months | IRB approval, partnerships |
| **Model Development** | 2-4 months | Can start with synthetic data |
| **Clinical Validation** | 6-12 months | Requires real data |
| **Regulatory Approval** | 3-18 months | Depends on intended use |
| **Total** | 14-40 months | Varies by regulatory path |

---

**Ready to replace?** Start with Option 2 (Synthetic but Realistic Data) or Option 1 (Pre-trained Model) for faster results while working toward the full clinical model.
