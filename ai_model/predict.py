# ai_model/predict.py
# Load and use the trained model for prediction

import tensorflow as tf
import numpy as np
import cv2
import json
import os
from PIL import Image

class PlantDiseasePredictor:
    def __init__(self, model_path='model/plant_disease_model.h5', class_names_path='model/class_names.json'):
        self.model_path = model_path
        self.class_names_path = class_names_path
        self.model = None
        self.class_names = []
        self.load_model()
        
    def load_model(self):
        """Load the trained model and class names"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, self.model_path)
        class_names_path = os.path.join(base_dir, self.class_names_path)
        
        if os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
            print(f"✅ Model loaded from {model_path}")
        else:
            print(f"❌ Model not found at {model_path}")
            return False
        
        if os.path.exists(class_names_path):
            with open(class_names_path, 'r') as f:
                self.class_names = json.load(f)
            print(f"✅ Loaded {len(self.class_names)} classes")
        else:
            print(f"❌ Class names not found at {class_names_path}")
            return False
        
        return True
    
    def preprocess_image(self, image):
        """Preprocess image for prediction (224x224 for MobileNetV2)"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Convert to RGB if needed
        if len(image.shape) == 2:  # Grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:  # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to 224x224 (MobileNetV2 requirement)
        image = cv2.resize(image, (224, 224))
        
        # Keep as float (model has built-in Rescaling layer)
        image = image.astype(np.float32)
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def predict(self, image):
        """Predict disease from image"""
        if self.model is None:
            return None, 0
        
        processed_image = self.preprocess_image(image)
        predictions = self.model.predict(processed_image, verbose=0)
        
        class_index = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]) * 100)
        
        predicted_class = self.class_names[class_index] if class_index < len(self.class_names) else "Unknown"
        
        return predicted_class, confidence

# ---------- TEST ----------
if __name__ == "__main__":
    predictor = PlantDiseasePredictor()
    if predictor.model is not None:
        print(f"✅ Predictor ready!")
        print(f"📋 Available classes: {predictor.class_names}")
    else:
        print("❌ Predictor not ready. Please check model files.")