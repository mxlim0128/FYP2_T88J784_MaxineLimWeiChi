"""
Phase 3 – Evaluate Seq2Point CNN (Washing Machine)
"""

import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error, f1_score

# -----------------------------
# Paths & parameters
# -----------------------------
DATA_PATH = "data/phase3/house1_washing_machine_seq2point.npz"
MODEL_PATH = "results/phase3/models/seq2point_washing_machine_best.h5"

APPLIANCE_MAX = 2500.0     # washing machine max power (W)
THRESHOLD_WATTS = 150.0    # ON/OFF threshold

# -----------------------------
# Load data
# -----------------------------
data = np.load(DATA_PATH)
X = data["X"]
y_true = data["y"]

X = X[..., np.newaxis]

# -----------------------------
# Load trained model
# -----------------------------
model = load_model(MODEL_PATH, compile=False)

# -----------------------------
# Predict
# -----------------------------
y_pred = model.predict(X).flatten()

# -----------------------------
# Regression metric (MAE)
# -----------------------------
mae = mean_absolute_error(
    y_true * APPLIANCE_MAX,
    y_pred * APPLIANCE_MAX
)

# -----------------------------
# Classification metric (F1)
# -----------------------------
threshold_norm = THRESHOLD_WATTS / APPLIANCE_MAX

y_true_bin = (y_true >= threshold_norm).astype(int)
y_pred_bin = (y_pred >= threshold_norm).astype(int)

f1 = f1_score(y_true_bin, y_pred_bin, zero_division=0)

# -----------------------------
# Output results
# -----------------------------
print(f"Seq2Point MAE (W): {mae:.3f}")
print(f"Seq2Point F1-score: {f1:.3f}")

with open("results/phase3/seq2point_washing_machine_metrics.txt", "w") as f:
    f.write(f"MAE (W): {mae:.3f}\n")
    f.write(f"F1-score: {f1:.3f}\n")

