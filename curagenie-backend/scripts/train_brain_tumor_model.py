"""
Brain Tumor Detection Model Trainer
Adapted from the GitHub Brain-Tumor-Detection repository

This script can train a CNN model for brain tumor detection using the architecture
defined in the Brain-Tumor-Detection repository.
"""

import os
import sys
import cv2
import imutils
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Input, ZeroPadding2D, BatchNormalization, Activation, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.utils import shuffle
from PIL import Image
import time
from os import listdir
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def crop_brain_contour(image, plot=False):
    """
    Crop the brain contour from the image - adapted from GitHub repository
    """
    try:
        # Convert the image to grayscale, and blur it slightly
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Threshold the image, then perform a series of erosions +
        # dilations to remove any small regions of noise
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours in thresholded image, then grab the largest one
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        # Find the extreme points
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        # crop new image out of the original image using the four extreme points
        new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]
        
        return new_image
    except:
        return image

def load_data(dir_list, image_size):
    """
    Read images, resize and normalize them - adapted from GitHub repository
    Arguments:
        dir_list: list of strings representing file directories.
    Returns:
        X: A numpy array with shape = (#_examples, image_width, image_height, #_channels)
        y: A numpy array with shape = (#_examples, 1)
    """
    
    # load all images in a directory
    X = []
    y = []
    image_width, image_height = image_size
    
    for directory in dir_list:
        if not os.path.exists(directory):
            logger.warning(f"Directory {directory} does not exist, skipping...")
            continue
            
        for filename in listdir(directory):
            try:
                # load the image
                image = cv2.imread(os.path.join(directory, filename))
                if image is None:
                    continue
                    
                # crop the brain and ignore the unnecessary rest part of the image
                image = crop_brain_contour(image, plot=False)
                # resize image
                image = cv2.resize(image, dsize=(image_width, image_height), interpolation=cv2.INTER_CUBIC)
                # normalize values
                image = image / 255.
                # convert image to numpy array and append it to X
                X.append(image)
                # append a value of 1 to the target array if the image
                # is in the folder named 'yes', otherwise append 0.
                if directory.endswith('yes'):
                    y.append([1])
                else:
                    y.append([0])
            except Exception as e:
                logger.warning(f"Error processing {filename}: {e}")
                continue
                
    X = np.array(X)
    y = np.array(y)
    
    # Shuffle the data
    X, y = shuffle(X, y)
    
    logger.info(f'Number of examples is: {len(X)}')
    logger.info(f'X shape is: {X.shape}')
    logger.info(f'y shape is: {y.shape}')
    
    return X, y

def build_model(input_shape):
    """
    Build the CNN model architecture from the GitHub repository
    Arguments:
        input_shape: A tuple representing the shape of the input of the model. shape=(image_width, image_height, #_channels)
    Returns:
        model: A Model object.
    """
    # Define the input placeholder as a tensor with shape input_shape. 
    X_input = Input(input_shape) # shape=(?, 240, 240, 3)
    
    # Zero-Padding: pads the border of X_input with zeroes
    X = ZeroPadding2D((2, 2))(X_input) # shape=(?, 244, 244, 3)
    
    # CONV -> BN -> RELU Block applied to X
    X = Conv2D(32, (7, 7), strides = (1, 1), name = 'conv0')(X)
    X = BatchNormalization(axis = 3, name = 'bn0')(X)
    X = Activation('relu')(X) # shape=(?, 238, 238, 32)
    
    # MAXPOOL
    X = MaxPooling2D((4, 4), name='max_pool0')(X) # shape=(?, 59, 59, 32) 
    
    # MAXPOOL
    X = MaxPooling2D((4, 4), name='max_pool1')(X) # shape=(?, 14, 14, 32)
    
    # FLATTEN X 
    X = Flatten()(X) # shape=(?, 6272)
    # FULLYCONNECTED
    X = Dense(1, activation='sigmoid', name='fc')(X) # shape=(?, 1)
    
    # Create model. This creates your Keras model instance, you'll use this instance to train/test the model.
    model = Model(inputs = X_input, outputs = X, name='BrainDetectionModel')
    
    return model

def compute_f1_score(y_true, prob):
    """Compute F1 score"""
    # convert the vector of probabilities to a target vector
    y_pred = np.where(prob > 0.5, 1, 0)
    
    score = f1_score(y_true, y_pred)
    
    return score

def create_dummy_data(output_dir="Brain-Tumor-Detection/dummy_data"):
    """
    Create dummy training data for demonstration purposes
    """
    os.makedirs(f"{output_dir}/yes", exist_ok=True)
    os.makedirs(f"{output_dir}/no", exist_ok=True)
    
    logger.info("Creating dummy training data...")
    
    # Create some dummy images with tumor-like patterns (bright spots)
    for i in range(50):
        # Create base brain-like image
        img = np.random.randint(20, 80, (240, 240, 3), dtype=np.uint8)
        
        # Add circular brain-like structure
        center = (120, 120)
        cv2.circle(img, center, 100, (60, 60, 60), -1)
        cv2.circle(img, center, 80, (80, 80, 80), -1)
        
        # For "yes" images, add bright tumor-like spots
        if i < 25:
            # Add tumor-like bright spots
            tumor_center = (np.random.randint(80, 160), np.random.randint(80, 160))
            cv2.circle(img, tumor_center, np.random.randint(10, 25), (200, 200, 200), -1)
            cv2.imwrite(f"{output_dir}/yes/tumor_{i}.jpg", img)
        else:
            # Normal brain images
            cv2.imwrite(f"{output_dir}/no/normal_{i-25}.jpg", img)
    
    logger.info(f"Created dummy data in {output_dir}")
    return f"{output_dir}/yes", f"{output_dir}/no"

def train_brain_tumor_model(data_dirs=None, model_save_path="models/brain_tumor_model.h5"):
    """
    Train the brain tumor detection model
    """
    logger.info("🧠 Starting Brain Tumor Detection Model Training...")
    
    # If no data directories provided, create dummy data
    if data_dirs is None:
        logger.info("No training data provided, creating dummy data...")
        yes_dir, no_dir = create_dummy_data()
        data_dirs = [yes_dir, no_dir]
    
    # Load data
    logger.info("Loading and preprocessing training data...")
    IMG_WIDTH, IMG_HEIGHT = (240, 240)
    X, y = load_data(data_dirs, (IMG_WIDTH, IMG_HEIGHT))
    
    if len(X) == 0:
        logger.error("No training data found!")
        return None
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logger.info(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
    
    # Build model
    logger.info("Building CNN model...")
    IMG_SHAPE = (IMG_WIDTH, IMG_HEIGHT, 3)
    model = build_model(IMG_SHAPE)
    
    # Compile model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    logger.info("Model architecture:")
    model.summary()
    
    # Setup callbacks
    os.makedirs("models", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # TensorBoard callback
    log_file_name = f'brain_tumor_detection_cnn_{int(time.time())}'
    tensorboard = TensorBoard(log_dir=f'logs/{log_file_name}')
    
    # Model checkpoint callback
    checkpoint = ModelCheckpoint(
        model_save_path,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='max'
    )
    
    # Train model
    logger.info("Starting model training...")
    history = model.fit(
        X_train, y_train,
        batch_size=16,
        epochs=10,  # Reduced for demo
        validation_data=(X_test, y_test),
        callbacks=[tensorboard, checkpoint],
        verbose=1
    )
    
    # Evaluate model
    logger.info("Evaluating model...")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    # Compute F1 score
    y_pred_prob = model.predict(X_test)
    f1 = compute_f1_score(y_test, y_pred_prob)
    
    logger.info(f"✅ Training completed!")
    logger.info(f"   - Test Accuracy: {test_accuracy:.4f}")
    logger.info(f"   - Test Loss: {test_loss:.4f}")
    logger.info(f"   - F1 Score: {f1:.4f}")
    logger.info(f"   - Model saved to: {model_save_path}")
    
    return model, history

if __name__ == "__main__":
    """
    Train the brain tumor detection model
    
    Usage:
    python scripts/train_brain_tumor_model.py
    
    Or with custom data directories:
    python scripts/train_brain_tumor_model.py path/to/yes path/to/no
    """
    
    # Check command line arguments
    if len(sys.argv) > 2:
        yes_dir = sys.argv[1]
        no_dir = sys.argv[2]
        
        if os.path.exists(yes_dir) and os.path.exists(no_dir):
            data_dirs = [yes_dir, no_dir]
            logger.info(f"Using provided data directories: {data_dirs}")
        else:
            logger.error("Provided directories do not exist!")
            data_dirs = None
    else:
        data_dirs = None
    
    # Train the model
    try:
        model, history = train_brain_tumor_model(data_dirs)
        
        if model is not None:
            logger.info("🎉 Brain tumor detection model training completed successfully!")
        else:
            logger.error("❌ Model training failed!")
            
    except Exception as e:
        logger.error(f"❌ Training failed with error: {e}")
        import traceback
        traceback.print_exc()
