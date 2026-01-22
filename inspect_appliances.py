from nilmtk import DataSet

ds = DataSet("data/processed/refit.h5")
elec = ds.buildings[1].elec

print("Appliances in House 1:\n")

for i, meter in enumerate(elec.submeters().meters):
    print(f"Meter {i}:")
    for app in meter.appliances:
        print("  -", app.type)

ds.store.close()
