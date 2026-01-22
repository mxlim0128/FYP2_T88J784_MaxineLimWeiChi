"""
Phase 3 – Train Seq2Point CNN (Washing Machine)
"""

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Flatten

# -----------------------------
# Load prepared data
# -----------------------------
data = np.load("data/phase3/house1_washing_machine_seq2point.npz")
X, y = data["X"], data["y"]

# Add channel dimension
X = X[..., np.newaxis]

# -----------------------------
# Build Seq2Point model
# -----------------------------
model = Sequential([
    Conv1D(30, 10, activation="relu", input_shape=(X.shape[1], 1)),
    Conv1D(30, 8, activation="relu"),
    Conv1D(40, 6, activation="relu"),
    Flatten(),
    Dense(1024, activation="relu"),
    Dense(1)
])

model.compile(
    optimizer="adam",
    loss="mse"
)

# -----------------------------
# Train model
# -----------------------------
model.fit(
    X, y,
    epochs=10,          # keep small (CPU)
    batch_size=64,
    validation_split=0.2
)

# -----------------------------
# Save model
# -----------------------------
model.save("results/phase3/models/seq2point_washing_machine_best.h5")
print("✔ Seq2Point model saved")
