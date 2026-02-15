import joblib
import numpy as np

def load_model():
    return joblib.load("model.pkl")

def predict_risk(model, data):
    input_data = np.array([data])
    prediction = model.predict(input_data)[0]

    risk_map = {
        0: "Low Risk",
        1: "Medium Risk",
        2: "High Risk"
    }

    return risk_map[prediction]
