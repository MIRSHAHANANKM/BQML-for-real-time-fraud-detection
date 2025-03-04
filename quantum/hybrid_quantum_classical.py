import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from quantum_fraud_detection import QuantumFraudDetector

# Generate synthetic fraud dataset
X = np.array([[5000, 0.8, 0.9, 1], [100, 0.1, 0.2, 0], [7000, 0.9, 1.0, 1], [50, 0.05, 0.1, 0]])
y = np.array([1, 0, 1, 0])  # 1 = Fraud, 0 = Legit

# Normalize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Convert to PyTorch tensors
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
X_train_torch = torch.tensor(X_train, dtype=torch.float32)
y_train_torch = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1)

# Initialize Quantum Model
quantum_model = QuantumFraudDetector(n_qubits=4, n_layers=2)
optimizer = optim.Adam(quantum_model.parameters(), lr=0.01)
loss_fn = nn.BCELoss()

# Training loop
for epoch in range(50):
    optimizer.zero_grad()
    predictions = quantum_model(X_train_torch)
    loss = loss_fn(predictions, y_train_torch)
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch}: Loss = {loss.item()}")

# Save trained model
torch.save(quantum_model.state_dict(), "quantum_fraud_model.pth")

print("Model saved!")