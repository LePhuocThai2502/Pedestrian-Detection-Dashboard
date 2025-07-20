import torch
from ultralytics import YOLO
import numpy as np

class PedestrianDetector:
    def __init__(self, model_path="models/yolov8n.pt", use_gpu=True):
        # Tự động dùng GPU nếu có
        device = "cuda" if torch.cuda.is_available() and use_gpu else "cpu"
        self.model = YOLO(model_path)
        self.model.to(device)

    def detect(self, img, conf=0.3):
        # Chỉ detect class person (COCO: class_id=0)
        results = self.model(img, conf=conf, classes=[0], verbose=False)
        return results[0]
