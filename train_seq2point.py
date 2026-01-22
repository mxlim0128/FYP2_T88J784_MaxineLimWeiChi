"""
Phase 3B – Seq2Point CNN Training
Appliance: Fridge
Dataset: REFIT – House 1 ONLY
"""

import os
import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# ==============================
# Configuration
# ==============================
DATA_DIR = "data/phase3"
MODEL_DIR = "results/phase3/models"

WINDOW_LENGTH = 599
BATCH_SIZE = 128
EPOCHS = 20
LEARNING_RATE = 0.001

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = f"{MODEL_DIR}/seq2point_fridge_best.h5"

# ==============================
# Load House 1 data
# ==============================
print("\n📥 Loading House 1 dataset...")
data = np.load(f"{DATA_DIR}/house1_fridge_seq2point.npz")
X = data["X"]
y = data["y"]

X = X[..., np.newaxis]

# Train / validation split (80/20)
split = int(0.8 * len(X))
X_train, X_val = X[:split], X[split:]
y_train, y_val = y[:split], y[split:]

print("Train shape:", X_train.shape)
print("Val shape  :", X_val.shape)

# ==============================
# Seq2Point CNN Model
# ==============================
model = Sequential([
    Conv1D(30, 10, activation="relu", input_shape=(WINDOW_LENGTH, 1)),
    Conv1D(30, 8, activation="relu"),
    Conv1D(40, 6, activation="relu"),
    Conv1D(50, 5, activation="relu"),
    Flatten(),
    Dense(1024, activation="relu"),
    Dense(1)
])

model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss="mse"
)

model.summary()

# ==============================
# Training
# ==============================
checkpoint = ModelCheckpoint(
    MODEL_PATH,
    save_best_only=True,
    monitor="val_loss",
    verbose=1
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

print("\n🚀 Training started...")

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=[checkpoint, early_stop]
)

print("\n✅ Training complete")
print(f"💾 Best model saved at {MODEL_PATH}")

# ==============================
# Save training history (for plots)
# ==============================
os.makedirs("results/phase3", exist_ok=True)

with open("results/phase3/training_history.json", "w") as f:
    json.dump(history.history, f)

print("📈 Training history saved")

