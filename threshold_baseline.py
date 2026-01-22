import numpy as np

# =========================
# Configuration
# =========================
DATA_PATH = "data/phase3/house1_fridge_seq2point.npz"

# =========================
# Load data
# =========================
data = np.load(DATA_PATH)

X = data["x"]      # shape: (samples, window)
y = data["y"]      # shape: (samples,)

print("Total samples:", X.shape[0])

# =========================
# Train / Test split (same as Seq2Point)
# =========================
split = int(0.8 * len(X))

X_val = X[split:]
y_val = y[split:]

print("Test samples:", X_val.shape[0])

# =========================
# Threshold-based NILM
# =========================
# Use mean appliance power as threshold
threshold = np.mean(y)

print("Threshold value:", round(threshold, 4))

# Prediction:
# If mean aggregate power > threshold → appliance ON
# Else → OFF
y_pred = np.where(X_val.mean(axis=1) > threshold, threshold, 0)

# =========================
# MAE calculation
# =========================
mae = np.mean(np.abs(y_pred - y_val))

print("Threshold-based NILM MAE:", round(mae, 4))
