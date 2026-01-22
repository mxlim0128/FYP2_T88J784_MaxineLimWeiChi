# file: src/eval/evaluate_nilm.py

import argparse
import yaml
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import f1_score, mean_absolute_error
import os

from src.models.seq2point import build_seq2point_model
from src.data.data_loader import load_and_preprocess_data


def evaluate(config):
    print("=== Starting FINAL NILM Evaluation ===")

    # Load test data
    X_test, y_test = load_and_preprocess_data(
        config,
        mode="test"   # IMPORTANT: test houses only
    )

    # Load model
    model = build_seq2point_model(
        input_shape=(config['window_size'], 1)
    )
    model.load_weights(
        os.path.join(config['checkpoint_dir'], "model.best.h5")
    )

    # Run inference
    y_pred = model.predict(X_test, verbose=1).flatten()

    # Denormalise appliance power
    y_pred_real = y_pred * config['APPLIANCE_MAX']
    y_true_real = y_test * config['APPLIANCE_MAX']

    # Compute MAE
    mae = mean_absolute_error(y_true_real, y_pred_real)

    # Compute F1-score (ON/OFF)
    threshold = config.get("power_threshold", 15.0)
    y_true_bin = (y_true_real >= threshold).astype(int)
    y_pred_bin = (y_pred_real >= threshold).astype(int)
    f1 = f1_score(y_true_bin, y_pred_bin)

    print("\n=== FINAL METRICS ===")
    print(f"MAE (W): {mae:.2f}")
    print(f"F1-score: {f1:.4f}")

    # Save results
    os.makedirs("results/tables", exist_ok=True)
    results_df = pd.DataFrame({
        "MAE_W": [mae],
        "F1_score": [f1]
    })
    results_df.to_csv(
        "results/tables/nilm_metrics_fridge.csv",
        index=False
    )

    print("Results saved to results/tables/nilm_metrics_fridge.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Final NILM evaluation")
    parser.add_argument(
        "--config", type=str, required=True,
        help="Path to YAML config file"
    )
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    evaluate(config)
