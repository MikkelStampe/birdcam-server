import torch
from torchvision import models, transforms
from PIL import Image
import json

# Load model + labels
model = models.efficientnet_b0(pretrained=True)
model.eval()

with open("imagenet_classes.txt") as f:
    labels = [line.strip() for line in f.readlines()]

# Preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225])
])

def classify_bird(image_path):
    image = Image.open(image_path).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0)  # add batch dim

    with torch.no_grad():
        output = model(input_tensor)
    probs = torch.nn.functional.softmax(output[0], dim=0)
    top_prob, top_idx = torch.topk(probs, 1)

    return f"{labels[top_idx.item()]} ({top_prob.item()*100:.1f}%)"