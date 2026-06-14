from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf


app = Flask(__name__)


# ==========================================
# LOAD TFLITE MODELS
# ==========================================


MODELS = {
    "laptop": "Seq2point/laptop_seq2point.tflite",
    "kettle": "Seq2point/kettle_seq2point.tflite",
    "lamp": "Seq2point/lamp_seq2point.tflite",
    "toaster": "Seq2point/toaster_seq2point.tflite"
}


interpreters = {}


for appliance, model_path in MODELS.items():


    print(f"Loading {appliance} model...")


    interpreter = tf.lite.Interpreter(
        model_path=model_path
    )


    interpreter.allocate_tensors()


    interpreters[appliance] = interpreter


print("All models loaded successfully.")


# ==========================================
# WINDOW SIZE
# ==========================================


WINDOW_SIZE = 599


# ==========================================
# PREDICT FUNCTION
# ==========================================


def predict_appliance(appliance, power_array):


    interpreter = interpreters[appliance]


    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()


    x = np.array(
        power_array,
        dtype=np.float32
    )


    x = x.reshape(
        1,
        WINDOW_SIZE,
        1
    )


    interpreter.set_tensor(
        input_details[0]['index'],
        x
    )


    interpreter.invoke()


    prediction = interpreter.get_tensor(
        output_details[0]['index']
    )


    pred_power = float(
        prediction[0][0]
    )


    if pred_power < 0:
        pred_power = 0


    return round(
        pred_power,
        2
    )


# ==========================================
# API ROUTE
# ==========================================


@app.route('/predict', methods=['POST'])
def predict():


    try:


        data = request.json


        print("\n========== NEW REQUEST ==========")
        print("DATA RECEIVED:")
        print(data)


        power_array = data.get("power", [])


        print("RECEIVED LENGTH =", len(power_array))


        # Validation
        if not isinstance(power_array, list):


            return jsonify({
                "error": "power must be array"
            }), 400


        if len(power_array) != WINDOW_SIZE:


            return jsonify({
                "error": f"expected {WINDOW_SIZE} samples"
            }), 400


        # Debug Information
        print("\n===== INPUT STATS =====")
        print("MIN =", np.min(power_array))
        print("MAX =", np.max(power_array))
        print("MEAN =", np.mean(power_array))


        status = {}
        power = {}


        # ==================================
        # RUN ALL MODELS
        # ==================================


        for appliance in MODELS.keys():


            pred_power = predict_appliance(
                appliance,
                power_array
            )


            power[appliance] = pred_power


            print(f"{appliance}: {pred_power:.2f} W")


            # ==================================
            # APPLIANCE STATUS THRESHOLDS
            # ==================================


            if appliance == "lamp":


                status[appliance] = 1 if pred_power > 12 else 0
                
            elif appliance == "kettle":


                status[appliance] = 1 if pred_power > 75 else 0
                
            elif appliance == "toaster":


                status[appliance] = 1 if pred_power > 100 else 0


            elif appliance == "laptop":


                status[appliance] = 1 if pred_power > 25 else 0



        print("\n===== PREDICTIONS =====")
        print(power)


        print("\n===== STATUS =====")
        print(status)


        result = {
            "status": status,
            "power": power
        }


        print("\nRESULT:")
        print(result)


        return jsonify(result)


    except Exception as e:


        print("\nERROR OCCURRED:")
        print(str(e))


        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# MAIN
# ==========================================


if __name__ == '__main__':


    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )


