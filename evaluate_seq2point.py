"""
Phase 3B – Evaluate Seq2Point CNN (House 1)
"""

import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error, f1_score

DATA_PATH = "data/phase3/house1_fridge_seq2point.npz"
MODEL_PATH = "results/phase3/models/seq2point_fridge_best.h5"

APPLIANCE_MAX = 1466.0   # for threshold normalization

# -----------------------------
# Load data
# -----------------------------
data = np.load(DATA_PATH)
X, y_true = data["X"], data["y"]

X = X[..., np.newaxis]

model = load_model(MODEL_PATH, compile=False)

# -----------------------------
# Predict
# -----------------------------
print("🔹 Running inference...")
y_pred = model.predict(X).flatten()

# -----------------------------
# Metrics
# -----------------------------
mae = mean_absolute_error(y_true * APPLIANCE_MAX,
                          y_pred * APPLIANCE_MAX)

# Normalized threshold (50 W)
threshold = 50.0 / APPLIANCE_MAX

y_true_bin = (y_true >= threshold).astype(int)
y_pred_bin = (y_pred >= threshold).astype(int)

f1 = f1_score(y_true_bin, y_pred_bin)

# -----------------------------
# Save results
# -----------------------------
with open("results/phase3/seq2point_metrics.txt", "w") as f:
    f.write(f"MAE (W): {mae:.3f}\n")
    f.write(f"F1-score: {f1:.3f}\n")

print("✔ MAE (W):", mae)
print("✔ F1-score:", f1)
print("📄 Results saved")

