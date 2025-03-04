import pennylane as qml
import torch
import torch.nn as nn
import numpy as np

# Define Quantum Device (Simulated Backend)
n_qubits = 4
dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev, interface="torch")
def quantum_circuit(inputs, weights):
    qml.templates.AngleEmbedding(inputs, wires=range(n_qubits))
    qml.templates.StronglyEntanglingLayers(weights, wires=range(n_qubits))
    return qml.expval(qml.PauliZ(0))  # ✅ Return a single value instead of multiple


class QuantumFraudDetector(nn.Module):
    def __init__(self, n_qubits, n_layers):
        super().__init__()
        weight_shapes = {"weights": (n_layers, n_qubits, 3)}
        self.qnode = qml.qnn.TorchLayer(quantum_circuit, weight_shapes)
        self.classifier = nn.Sequential(
            nn.Linear(1, 1),  # ✅ Ensure input is 1, output is 1
            nn.Sigmoid()
        )

    def forward(self, x):
        q_output = self.qnode(x).unsqueeze(1)  # ✅ Ensure shape is [batch_size, 1]
        return self.classifier(q_output)


# Initialize Model
model = QuantumFraudDetector(n_qubits=4, n_layers=2)
test_input = torch.tensor([[0.1, 0.2, 0.3, 0.4]], dtype=torch.float32)

# Forward Pass
output = model(test_input)
print("Quantum Fraud Detection Output:", output)

