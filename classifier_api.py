from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np


app = Flask(__name__)


# ==========================================
# LOAD CLASSIFIER MODELS
# ==========================================


MODELS = {
    "kettle": "Classifier/kettle_classifier.tflite",
    "toaster": "Classifier/toaster_classifier.tflite",
    "laptop": "Classifier/laptop_classifier.tflite",
    "lamp": "Classifier/lamp_classifier.tflite"
}


interpreters = {}


for appliance, model_path in MODELS.items():


    print(f"Loading {appliance} classifier...")


    interpreter = tf.lite.Interpreter(
        model_path=model_path
    )


    interpreter.allocate_tensors()


    interpreters[appliance] = interpreter


print("All classifier models loaded.")


# ==========================================
# WINDOW SIZE
# ==========================================


WINDOW_SIZE = 599


# ==========================================
# PREDICT FUNCTION
# ==========================================


def predict_classifier(appliance, power_array):


    interpreter = interpreters[appliance]


    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()


    x = np.array(
        power_array,
        dtype=np.float32
    )


    # KETTLE MODEL
    if appliance == "kettle":


        x = x.reshape(
            1,
            WINDOW_SIZE,
            1
        )


    # TOASTER / LAPTOP / LAMP
    else:


        x = np.stack(
            [x, x],
            axis=-1
        )


        x = x.reshape(
            1,
            WINDOW_SIZE,
            2
        )


    interpreter.set_tensor(
        input_details[0]['index'],
        x
    )


    interpreter.invoke()


    prediction = interpreter.get_tensor(
        output_details[0]['index']
    )


    return float(prediction[0][0])


# ==========================================
# API
# ==========================================


@app.route('/classify', methods=['POST'])
def classify():


    try:


        data = request.json


        power_array = data.get("power", [])


        if not isinstance(power_array, list):


            return jsonify({
                "error": "power must be array"
            }), 400


        if len(power_array) != WINDOW_SIZE:


            return jsonify({
                "error": f"expected {WINDOW_SIZE} samples"
            }), 400


        probabilities = {}
        status = {}


        for appliance in MODELS.keys():


            prob = predict_classifier(
                appliance,
                power_array
            )


            probabilities[appliance] = round(prob, 6)


            status[appliance] = 1 if prob > 0.5 else 0


        result = {
            "probability": probabilities,
            "status": status
        }


        print(result)


        return jsonify(result)


    except Exception as e:


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
        port=5001,
        debug=True
    )




from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf


app = Flask(__name__)


# ==========================================
# LOAD CLASSIFIER MODELS
# ==========================================


MODELS = {
    "laptop": "Classifier/laptop_classifier.tflite",
    "kettle": "Classifier/kettle_classifier.tflite",
    "lamp": "Classifier/lamp_classifier.tflite",
    "toaster": "Classifier/toaster_classifier.tflite"
}


interpreters = {}


for appliance, path in MODELS.items():


    print(f"Loading {appliance} classifier...")


    interpreter = tf.lite.Interpreter(model_path=path)
    interpreter.allocate_tensors()


    interpreters[appliance] = interpreter


print("All classifiers loaded.")


# ==========================================
# WINDOW SIZE
# ==========================================


WINDOW_SIZE = 599


# ==========================================
# CLASSIFIER FUNCTION
# ==========================================


def classify_appliance(appliance, power_array):


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


    probability = float(prediction[0][0])


    return round(probability, 4)


# ==========================================
# API
# ==========================================


@app.route('/predict', methods=['POST'])
def predict():


    try:


        data = request.json


        power_array = data.get("power", [])


        if not isinstance(power_array, list):
            return jsonify({
                "error": "power must be array"
            }), 400


        if len(power_array) != WINDOW_SIZE:
            return jsonify({
                "error": f"expected {WINDOW_SIZE} samples"
            }), 400


        print("\n===== INPUT =====")
        print("MIN =", np.min(power_array))
        print("MAX =", np.max(power_array))
        print("MEAN =", np.mean(power_array))


        probabilities = {}


        for appliance in MODELS.keys():


            prob = classify_appliance(
                appliance,
                power_array
            )


            probabilities[appliance] = prob


            print(
                appliance,
                "=",
                prob
            )


        # =====================================
        # FIND HIGHEST PROBABILITY
        # =====================================


        detected = max(
            probabilities,
            key=probabilities.get
        )


        status = {
            "lamp": 0,
            "laptop": 0,
            "kettle": 0,
            "toaster": 0
        }


        status[detected] = 1


        result = {
            "detected_appliance": detected,
            "probabilities": probabilities,
            "status": status
        }


        print("\n===== RESULT =====")
        print(result)


        return jsonify(result)


    except Exception as e:


        print("ERROR:", str(e))


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
