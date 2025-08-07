#!/usr/bin/env python3
"""
Setup ML Models for CuraGenie Deployment
This script creates minimal ML models for deployment when the original large models
cannot be included in the repository due to size constraints.
"""

import os
import pickle
import numpy as np

# Try to import ML dependencies, create placeholders if not available
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.datasets import make_classification
    SKLEARN_AVAILABLE = True
except ImportError:
    print("⚠️ Scikit-learn not available, creating placeholder models")
    SKLEARN_AVAILABLE = False

try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("⚠️ TensorFlow not available, creating placeholder models")
    TENSORFLOW_AVAILABLE = False

def create_models_directory():
    """Create models directory if it doesn't exist."""
    os.makedirs('models', exist_ok=True)
    print("✅ Created models directory")

def create_brain_tumor_model():
    """Create a minimal CNN model for brain tumor detection."""
    if not TENSORFLOW_AVAILABLE:
        # Create placeholder file
        with open('models/brain_tumor_model.h5', 'w') as f:
            f.write("# Placeholder model file - TensorFlow not available during build")
        print("⚠️ Created placeholder brain tumor model (TensorFlow not available)")
        return
        
    try:
        # Create a simple CNN model
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(4, activation='softmax')  # 4 classes: glioma, meningioma, notumor, pituitary
        ])
        
        model.compile(optimizer='adam',
                     loss='sparse_categorical_crossentropy',
                     metrics=['accuracy'])
        
        # Save the model
        model.save('models/brain_tumor_model.h5')
        print("✅ Created brain tumor detection model")
        
    except Exception as e:
        print(f"❌ Error creating brain tumor model: {e}")
        # Create a dummy file as fallback
        with open('models/brain_tumor_model.h5', 'w') as f:
            f.write("# Placeholder model file - replace with actual trained model")

def create_sklearn_models():
    """Create minimal sklearn models for other predictions."""
    
    model_names = ['alzheimer_model.pkl', 'diabetes_model.pkl', 'diabetes_risk_model.pkl']
    
    if not SKLEARN_AVAILABLE:
        # Create placeholder files
        for model_name in model_names:
            with open(f'models/{model_name}', 'wb') as f:
                pickle.dump({'error': 'placeholder model - scikit-learn not available'}, f)
            print(f"⚠️ Created placeholder {model_name} (scikit-learn not available)")
        return
    
    try:
        # Create synthetic datasets
        X_alzheimer, y_alzheimer = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
        X_diabetes, y_diabetes = make_classification(n_samples=1000, n_features=8, n_classes=2, random_state=42)
        
        # Train simple models
        models = {
            'alzheimer_model.pkl': RandomForestClassifier(n_estimators=50, random_state=42),
            'diabetes_model.pkl': RandomForestClassifier(n_estimators=50, random_state=42),
            'diabetes_risk_model.pkl': RandomForestClassifier(n_estimators=50, random_state=42)
        }
        
        datasets = {
            'alzheimer_model.pkl': (X_alzheimer, y_alzheimer),
            'diabetes_model.pkl': (X_diabetes, y_diabetes),
            'diabetes_risk_model.pkl': (X_diabetes, y_diabetes)
        }
        
        for model_name, model in models.items():
            try:
                X, y = datasets[model_name]
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # Train the model
                model.fit(X_train, y_train)
                
                # Save the model
                with open(f'models/{model_name}', 'wb') as f:
                    pickle.dump(model, f)
                    
                accuracy = model.score(X_test, y_test)
                print(f"✅ Created {model_name} (accuracy: {accuracy:.2f})")
                
            except Exception as e:
                print(f"❌ Error creating {model_name}: {e}")
                # Create placeholder file
                with open(f'models/{model_name}', 'wb') as f:
                    pickle.dump({'error': 'placeholder model'}, f)
                    
    except Exception as e:
        print(f"❌ Error in sklearn models setup: {e}")
        # Create placeholder files for all models
        for model_name in model_names:
            with open(f'models/{model_name}', 'wb') as f:
                pickle.dump({'error': 'placeholder model'}, f)

def create_uploads_directory():
    """Create uploads directory for file uploads."""
    os.makedirs('uploads', exist_ok=True)
    print("✅ Created uploads directory")

def main():
    """Main setup function."""
    print("🚀 Setting up CuraGenie ML Models for Deployment")
    print("=" * 50)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Create necessary directories
    create_models_directory()
    create_uploads_directory()
    
    # Create ML models
    print("\n📦 Creating ML Models...")
    create_brain_tumor_model()
    create_sklearn_models()
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Models created:")
    print("• models/brain_tumor_model.h5 - Brain tumor detection")
    print("• models/alzheimer_model.pkl - Alzheimer's prediction")
    print("• models/diabetes_model.pkl - Diabetes prediction")
    print("• models/diabetes_risk_model.pkl - Diabetes risk assessment")
    print("\n💡 Note: These are minimal models for deployment.")
    print("   Replace with your trained models for production use.")

if __name__ == "__main__":
    main()
