from flask import Flask, request, jsonify
import torch
from quantum_fraud_detection import QuantumFraudDetector

app = Flask(__name__)

# Load trained quantum model
quantum_model = QuantumFraudDetector(n_qubits=4, n_layers=2)
quantum_model.load_state_dict(torch.load("quantum_fraud_model.pth"))
quantum_model.eval()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    transaction = torch.tensor([data["amount"], data["risk_factor"], data["user_behavior"], data["flag"]], dtype=torch.float32).unsqueeze(0)
    
    prediction = quantum_model(transaction).item()
    is_fraud = prediction > 0.5
    return jsonify({"fraud_probability": prediction, "is_fraud": is_fraud})

if __name__ == "__main__":
    app.run(debug=True)
