import os
from PIL import Image
import numpy as np
import cv2
import tempfile
import shutil
import time

from src.config import HISTORY_PATH

def save_temp_image(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB")
    tmp_path = os.path.join(tempfile.gettempdir(), f"pd_temp_{time.time_ns()}.jpg")
    img.save(tmp_path)
    return tmp_path

def draw_boxes(result, color=(255,0,0)):
    image = np.array(result.orig_img).copy()
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        label = f'Person {conf:.2f}'
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return Image.fromarray(image)

def save_history(image, filename, num_person, tab="image"):
    date = time.strftime("%Y-%m-%d_%H-%M-%S")
    save_dir = os.path.join(HISTORY_PATH, tab)
    os.makedirs(save_dir, exist_ok=True)
    # Lưu ảnh
    save_path = os.path.join(save_dir, f"{date}_{num_person}_{filename}")
    image.save(save_path)
    # Lưu log
    log_path = os.path.join(save_dir, "log.csv")
    import pandas as pd
    df = pd.DataFrame([{
        "time": date,
        "file": filename,
        "num_person": num_person
    }])
    if os.path.exists(log_path):
        df.to_csv(log_path, mode="a", header=False, index=False)
    else:
        df.to_csv(log_path, mode="w", header=True, index=False)
    return save_path


def clear_temp_files(prefix="pd_temp_"):
    tmpdir = tempfile.gettempdir()
    for fname in os.listdir(tmpdir):
        if fname.startswith(prefix):
            try:
                os.remove(os.path.join(tmpdir, fname))
            except: pass
