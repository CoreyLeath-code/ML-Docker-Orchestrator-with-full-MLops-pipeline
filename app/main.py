# app/main.py

"""
FastAPI app to load the trained PyTorch model and expose a prediction endpoint.
Use this inside a Docker container for local or cloud-based inference.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import torch
import torch.nn as nn
import numpy as np

app = FastAPI()

# Define model architecture again (must match train.py)
class SimpleNet(nn.Module):
    def __init__(self, input_dim):
        super(SimpleNet, self).__init__()
        self.layer1 = nn.Linear(input_dim, 64)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(64, 2)

    def forward(self, x):
        x = self.relu(self.layer1(x))
        return self.layer2(x)

# Load model
model = SimpleNet(input_dim=20)
model.load_state_dict(torch.load("model/model.pth", map_location="cpu"))
model.eval()

# Input schema using Pydantic
class InferenceRequest(BaseModel):
    features: list  # expects a list of 20 numerical features

@app.get("/")
def health_check():
    return {"status": "Model is up and running."}

@app.post("/predict")
def predict(request: InferenceRequest):
    with torch.no_grad():
        input_tensor = torch.FloatTensor(np.array(request.features).reshape(1, -1))
        output = model(input_tensor)
        prediction = torch.argmax(output, dim=1).item()
        return {"prediction": prediction}
