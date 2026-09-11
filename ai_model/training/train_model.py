# ai_model/training/train_model.py
# Plant Disease Detection - Transfer Learning (MobileNetV2) with Fine-Tuning

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
import os
import json

# ---------- CONFIGURATION ----------
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 30
LEARNING_RATE = 0.00001         # Changed: 0.0001 → 0.00001 (10x kam)

# ---------- DATA LOADING ----------
print("📂 Loading dataset...")

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    '../data/train',
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    '../data/train',
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
print(f"📋 Classes: {class_names}")

os.makedirs('../model', exist_ok=True)
with open('../model/class_names.json', 'w') as f:
    json.dump(class_names, f)
print("✅ Class names saved")

# ---------- DATA AUGMENTATION ----------
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.15),
    layers.RandomContrast(0.1),
])

train_ds = train_ds.map(
    lambda x, y: (data_augmentation(x, training=True), y),
    num_parallel_calls=tf.data.AUTOTUNE
)

train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

# ---------- BUILD MODEL (Transfer Learning + Fine-Tuning) ----------
print("🏗️ Building model with MobileNetV2...")

base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# 🔑 FINE-TUNING: Unfreeze last 30 layers
base_model.trainable = True
for layer in base_model.layers[:-30]:
    layer.trainable = False

print(f"✅ Trainable layers: {sum([1 for l in base_model.layers if l.trainable])}/{len(base_model.layers)}")

model = models.Sequential([
    layers.Rescaling(1./127.5, offset=-1, input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ---------- CALLBACKS ----------
callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        '../model/plant_disease_model.h5',
        save_best_only=True,
        monitor='val_accuracy',
        mode='max',
        verbose=1
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=7,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=0.000001
    )
]

# ---------- TRAIN ----------
print("🚀 Training started...")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks
)

# ---------- SAVE ----------
print("💾 Saving model...")
model.save('../model/plant_disease_model.h5')
print("✅ Model saved!")

with open('../model/training_history.json', 'w') as f:
    json.dump({
        'accuracy': history.history['accuracy'],
        'val_accuracy': history.history['val_accuracy'],
        'loss': history.history['loss'],
        'val_loss': history.history['val_loss']
    }, f)

print("\n🎉 Training complete!")
print(f"📋 Classes: {len(class_names)}")