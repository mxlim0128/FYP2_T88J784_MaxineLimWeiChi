from nilmtk import DataSet
from sklearn.metrics import mean_absolute_error, f1_score

DATA_PATH = "data/processed/refit.h5"
BUILDING_ID = 1
APPLIANCE_TYPE = "washing machine"
THRESHOLD = 150  # watts

print("Loading dataset...")
ds = DataSet(DATA_PATH)
elec = ds.buildings[BUILDING_ID].elec

print("Loading aggregate power...")
aggregate = elec.mains().power_series_all_data().dropna()

print("Finding washing machine submeter...")
washing_machine_meter = None
for meter in elec.submeters().meters:
    for appliance in meter.appliances:
        if appliance.type == APPLIANCE_TYPE:
            washing_machine_meter = meter
            break

if washing_machine_meter is None:
    raise ValueError("Washing machine not found!")

print("Loading washing machine power...")
appliance_power = washing_machine_meter.power_series_all_data().dropna()

aggregate, appliance_power = aggregate.align(appliance_power, join="inner")

print("Applying threshold...")
predicted = aggregate.copy()
predicted[predicted < THRESHOLD] = 0

mae = mean_absolute_error(appliance_power, predicted)

y_true = (appliance_power > THRESHOLD).astype(int)
y_pred = (predicted > THRESHOLD).astype(int)

f1 = f1_score(y_true, y_pred, zero_division=0)

print("MAE (W):", round(mae, 3))
print("F1-score:", round(f1, 3))

ds.store.close()
