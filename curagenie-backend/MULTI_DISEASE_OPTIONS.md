# Multi-Disease Model Implementation Options

## Current Status
- **Single Model**: `diabetes_model.pkl` 
- **Single Prediction**: Generic risk prediction
- **Database**: `MlPrediction` table without disease type

## Option 1: Single Multi-Disease Model ⭐ RECOMMENDED

### What You Provide
```
File: multi_disease_model.pkl
Type: One model that handles all diseases
```

### Model Interface Required
```python
# Method 1: Disease as input feature (6 features total)
features = [age, bmi, glucose, bp, family_history, disease_code]
# disease_code: 0=diabetes, 1=alzheimer, 2=brain_tumor

prediction = model.predict([features])[0]     # 0 or 1
probabilities = model.predict_proba([features])[0]  # [prob_low, prob_high]

# Method 2: Disease as parameter to predict method  
prediction = model.predict([features], disease="diabetes")[0]
probabilities = model.predict_proba([features], disease="diabetes")[0]
```

### Code Changes Needed: MINIMAL
```python
# In worker/tasks.py - ONLY change the inference logic:

@celery_app.task(bind=True)
def run_ml_inference(self, user_id: str, clinical_data: dict, disease_type: str = "diabetes"):
    # Same feature extraction
    features = [
        clinical_data.get('age', 45),
        clinical_data.get('bmi', 25.0),
        clinical_data.get('glucose_level', 100),
        clinical_data.get('blood_pressure', 120),
        clinical_data.get('family_history', 0)
    ]
    
    # NEW: Add disease code
    disease_codes = {"diabetes": 0, "alzheimer": 1, "brain_tumor": 2}
    features.append(disease_codes.get(disease_type, 0))
    
    # Same prediction logic
    prediction = ML_MODEL.predict([features])[0]
    prediction_proba = ML_MODEL.predict_proba([features])[0]
    
    # Save with disease type
    ml_prediction = MlPrediction(
        user_id=user_id,
        prediction=f"{disease_type}: {'High Risk' if prediction else 'Low Risk'}",
        confidence=float(max(prediction_proba))
    )
```

### Advantages
- ✅ **Minimal changes**: ~10 lines of code
- ✅ **Single file**: Easy to manage
- ✅ **Consistent**: Same interface for all diseases
- ✅ **Efficient**: One model loaded in memory

---

## Option 2: Three Separate Models

### What You Provide
```
Files: 
- diabetes_model.pkl
- alzheimer_model.pkl  
- brain_tumor_model.pkl

Each model uses same 5 features, predicts its specific disease
```

### Model Interface Required (for each model)
```python
# Same 5 features for all models
features = [age, bmi, glucose, bp, family_history]

# Each model predicts its specific disease
diabetes_prediction = diabetes_model.predict([features])[0]
alzheimer_prediction = alzheimer_model.predict([features])[0]
tumor_prediction = brain_tumor_model.predict([features])[0]
```

### Code Changes Needed: MODERATE
```python
# In worker/tasks.py - Replace single model with multiple:

# Load all models at startup
DIABETES_MODEL = None
ALZHEIMER_MODEL = None
BRAIN_TUMOR_MODEL = None

def load_ml_models():
    global DIABETES_MODEL, ALZHEIMER_MODEL, BRAIN_TUMOR_MODEL
    
    # Load diabetes model
    if os.path.exists("models/diabetes_model.pkl"):
        with open("models/diabetes_model.pkl", 'rb') as f:
            DIABETES_MODEL = pickle.load(f)
    
    # Load alzheimer model  
    if os.path.exists("models/alzheimer_model.pkl"):
        with open("models/alzheimer_model.pkl", 'rb') as f:
            ALZHEIMER_MODEL = pickle.load(f)
            
    # Load brain tumor model
    if os.path.exists("models/brain_tumor_model.pkl"):
        with open("models/brain_tumor_model.pkl", 'rb') as f:
            BRAIN_TUMOR_MODEL = pickle.load(f)

@celery_app.task(bind=True)
def run_ml_inference(self, user_id: str, clinical_data: dict, disease_type: str = "diabetes"):
    # Same feature extraction
    features = [
        clinical_data.get('age', 45),
        clinical_data.get('bmi', 25.0),
        clinical_data.get('glucose_level', 100),
        clinical_data.get('blood_pressure', 120),
        clinical_data.get('family_history', 0)
    ]
    
    # NEW: Select model based on disease
    if disease_type == "diabetes":
        model = DIABETES_MODEL
    elif disease_type == "alzheimer":  
        model = ALZHEIMER_MODEL
    elif disease_type == "brain_tumor":
        model = BRAIN_TUMOR_MODEL
    else:
        raise Exception(f"Unknown disease type: {disease_type}")
    
    if model is None:
        raise Exception(f"Model for {disease_type} not loaded")
    
    # Use selected model
    prediction = model.predict([features])[0]
    prediction_proba = model.predict_proba([features])[0]
    
    # Save with disease type
    ml_prediction = MlPrediction(
        user_id=user_id,
        prediction=f"{disease_type}: {'High Risk' if prediction else 'Low Risk'}",
        confidence=float(max(prediction_proba))
    )
```

### Database Changes Needed
```python
# Update MlPrediction model to include disease type
class MlPrediction(Base):
    __tablename__ = 'ml_predictions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    disease_type = Column(String, index=True)  # NEW FIELD
    prediction = Column(String)
    confidence = Column(Float)
```

### API Changes Needed
```python
# Update API to accept disease type
@router.post("/predict/{disease_type}", status_code=202)
async def trigger_ml_prediction(
    disease_type: str,  # NEW PARAMETER
    request: MlInferenceRequest,
    db: Session = Depends(get_db)
):
    # Validate disease type
    if disease_type not in ["diabetes", "alzheimer", "brain_tumor"]:
        raise HTTPException(status_code=400, detail="Invalid disease type")
    
    # Queue with disease type
    run_ml_inference.delay(request.user_id, request.clinical_data, disease_type)
```

### Advantages
- ✅ **Specialized**: Each model optimized for specific disease
- ✅ **Independent**: Models can be updated separately  
- ✅ **Flexible**: Different features possible for each disease

### Disadvantages  
- ❌ **More complex**: ~50 lines of code changes
- ❌ **More files**: 3 files to manage
- ❌ **More memory**: 3 models loaded simultaneously
- ❌ **Database changes**: Need migration

---

## Option 3: Hybrid Approach

### What You Provide
```
Files:
- multi_disease_model.pkl (handles diabetes + alzheimer)
- brain_tumor_model.pkl (specialized for brain tumors)
```

### When to Use
- Brain tumor prediction needs different features (e.g., MRI data)
- Diabetes and Alzheimer can use same clinical features
- Best of both worlds

---

## Recommendation: Go with Option 1 ⭐

**Why Option 1 is best:**

1. **Easiest for you**: Train one model that handles all diseases
2. **Easiest for me**: Minimal code changes (~10 lines)
3. **Most efficient**: Single model, single file
4. **Future-proof**: Easy to add more diseases
5. **Consistent**: Same interface for all diseases

## Training Your Multi-Disease Model

```python
# Example training approach for Option 1
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Prepare training data
data = pd.read_csv("medical_data.csv")

# Features: age, bmi, glucose, bp, family_history, disease_type
X = data[['age', 'bmi', 'glucose', 'bp', 'family_history', 'disease_code']]
y = data['has_disease']  # 0/1 for each disease

# Train single model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
import pickle
with open('multi_disease_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

## What Should You Provide?

**For Option 1 (Recommended):**
```
✅ One file: multi_disease_model.pkl
✅ Model accepts 6 features: [age, bmi, glucose, bp, family_history, disease_code]
✅ Disease codes: 0=diabetes, 1=alzheimer, 2=brain_tumor
✅ Returns 0/1 prediction + probabilities for specified disease
```

**For Option 2:**
```
✅ Three files: diabetes_model.pkl, alzheimer_model.pkl, brain_tumor_model.pkl  
✅ Each model accepts 5 features: [age, bmi, glucose, bp, family_history]
✅ Each model predicts its specific disease only
```

## Testing Your Models

```python
# Test script for Option 1
model = pickle.load(open('multi_disease_model.pkl', 'rb'))

# Test diabetes prediction
diabetes_features = [45, 28.0, 110, 130, 1, 0]  # disease_code=0
diabetes_pred = model.predict([diabetes_features])[0]
print(f"Diabetes risk: {'High' if diabetes_pred else 'Low'}")

# Test alzheimer prediction  
alzheimer_features = [75, 25.0, 100, 140, 1, 1]  # disease_code=1
alzheimer_pred = model.predict([alzheimer_features])[0]
print(f"Alzheimer risk: {'High' if alzheimer_pred else 'Low'}")

# Test brain tumor prediction
tumor_features = [50, 26.0, 95, 120, 0, 2]  # disease_code=2
tumor_pred = model.predict([tumor_features])[0]
print(f"Brain tumor risk: {'High' if tumor_pred else 'Low'}")
```

---

**Which option do you prefer?** 

- **Option 1**: Single model for all diseases (recommended)
- **Option 2**: Three separate models 
- **Option 3**: Hybrid approach

Let me know and I'll implement the necessary changes!
