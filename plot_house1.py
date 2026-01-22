from nilmtk import DataSet
import matplotlib.pyplot as plt

# Load dataset
ds = DataSet("data/processed/refit.h5")
elec = ds.buildings[1].elec

def plot_meter(meter, title, filename):
    plt.figure(figsize=(10, 4))
    meter.plot()
    plt.title(title)
    plt.ylabel("Power (W)")
    plt.xlabel("Time")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# -------- Aggregate --------
plot_meter(
    elec.mains(),
    "House 1 – Aggregate Power",
    "house1_aggregate_power.png"
)

# -------- Appliance meters (explicit, no ambiguity) --------
meters = list(elec.submeters().meters)

# Inspect once (optional, but good)
for m in meters:
    print(m.appliances)

# Manual, explicit selection (REFIT House 1)
fridge = meters[0]
freezer = meters[1]
washing_machine = meters[2]

plot_meter(fridge, "House 1 – Fridge Power", "house1_fridge_power.png")
plot_meter(freezer, "House 1 – Freezer Power", "house1_freezer_power.png")
plot_meter(
    washing_machine,
    "House 1 – Washing Machine Power",
    "house1_washing_machine_power.png"
)

ds.store.close()
print("✔ Plots generated successfully")

