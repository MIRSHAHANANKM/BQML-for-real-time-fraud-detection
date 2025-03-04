import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from data_preprocessing import load_and_preprocess_data
from meta_learning_model import FraudMetaModel

# Load data
X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(r"meta_learning\Fraud_Data.csv")

# Convert to tensors
X_train_torch = torch.tensor(X_train, dtype=torch.float32)
y_train_torch = torch.tensor(np.array(y_train), dtype=torch.float32).reshape(-1, 1)


# Initialize meta-model
model = FraudMetaModel(input_size=X_train.shape[1])
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.BCELoss()

# Meta-learning training loop
def meta_train(model, optimizer, loss_fn, X_train, y_train, meta_steps=5, inner_lr=0.01):
    """Meta-learning using MAML for fraud detection"""
    for meta_step in range(meta_steps):
        cloned_model = FraudMetaModel(input_size=X_train.shape[1])  # Clone model for adaptation
        cloned_model.load_state_dict(model.state_dict())
        inner_optimizer = optim.SGD(cloned_model.parameters(), lr=inner_lr)

        # Inner loop: Train on few fraud samples
        for _ in range(3):
            inner_optimizer.zero_grad()
            predictions = cloned_model(X_train)
            loss = loss_fn(predictions, y_train)
            loss.backward()
            inner_optimizer.step()

        # Outer loop: Update meta-model using adapted model
        optimizer.zero_grad()
        meta_loss = loss_fn(model(X_train), y_train)
        meta_loss.backward()
        optimizer.step()

        if meta_step % 1 == 0:
            print(f"Meta-step {meta_step}: Loss = {meta_loss.item()}")

# Train meta-learning model
meta_train(model, optimizer, loss_fn, X_train_torch, y_train_torch)

# Save trained model
torch.save(model.state_dict(), "meta_fraud_model.pth")
