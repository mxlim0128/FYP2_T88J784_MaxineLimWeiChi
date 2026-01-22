import json
import matplotlib.pyplot as plt

# Load training history
with open("results/phase3/training_history.json", "r") as f:
    history = json.load(f)

plt.figure()
plt.plot(history["loss"], label="Training Loss")
plt.plot(history["val_loss"], label="Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.title("Seq2Point Training Curve")
plt.legend()
plt.grid(True)

# Save figure
plt.savefig("results/phase3/training_curve.png")
plt.show()
