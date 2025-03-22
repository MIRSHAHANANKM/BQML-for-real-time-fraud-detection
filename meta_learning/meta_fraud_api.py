from flask import Flask, request, jsonify
import torch
from meta_learning_model import FraudMetaModel
from data_preprocessing import scaler

app = Flask(__name__)

# Load trained meta-learning model
model = FraudMetaModel(input_size=10)
model.load_state_dict(torch.load("meta_fraud_model.pth"))
model.eval()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    transaction = torch.tensor(scaler.transform([[data["amount"], data["risk_score"], data["user_behavior"], data["device_trust"]]]), dtype=torch.float32)
    
    prediction = model(transaction).item()
    is_fraud = prediction > 0.5
    return jsonify({"fraud_probability": prediction, "is_fraud": is_fraud})

if __name__ == "__main__":
    app.run(debug=True, port=5500)
