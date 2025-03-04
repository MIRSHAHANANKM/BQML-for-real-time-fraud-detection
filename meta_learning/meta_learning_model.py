import torch
import torch.nn as nn
import torch.optim as optim

class FraudMetaModel(nn.Module):
    """Neural network for fraud detection with meta-learning (MAML)"""
    def __init__(self, input_size):
        super(FraudMetaModel, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

if __name__ == "__main__":
    # Sample code to test the model
    model = FraudMetaModel(input_size=10)  # Change input size as needed
    sample_input = torch.rand(1, 10)  # Random input tensor
    output = model(sample_input)
    print("Model Output:", output.item())
