import torch
import cv2
import os
import gdown
import numpy as np
import torchvision.transforms as transforms
from csrnet_model import CustomCSRNet
from yolo_people_counter import count_people_yolo

# ---------------- DEVICE ----------------
device = torch.device("cpu")

# ---------------- MODEL ----------------
MODEL_PATH = "best_finetuned.pth"
MODEL_URL = "https://drive.google.com/uc?export=download&id=1GHhLvz9uZYnT9EOtqGHKi5sC7AQhO-F0"

def download_model():
    import requests

    print("Downloading model...")

    url = "https://drive.google.com/uc?export=download&id=1GHhLvz9uZYnT9EOtqGHKi5sC7AQhO-F0"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    except Exception as e:
        raise RuntimeError(f"Model download failed: {e}")
    # check if file actually downloaded
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file not found after download!")

# ---------------- ENSURE MODEL ----------------
if not os.path.exists(MODEL_PATH):
    download_model()

# ---------------- LOAD MODEL ----------------
try:
    csrnet = CustomCSRNet().to(device)
    csrnet.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    csrnet.eval()
except Exception as e:
    raise RuntimeError(f"Model loading failed: {e}")

# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ---------------- CALIBRATION ----------------
SPARSE_CALIBRATION = 0.2

# ---------------- MAIN FUNCTION ----------------
def run_density(frame, is_webcam=False):

    resized = cv2.resize(frame, (640, 480))
    img = transform(resized).unsqueeze(0).to(device)

    with torch.no_grad():
        density = csrnet(img)[0, 0].cpu().numpy()

    csr_count = float(density.sum())
    yolo_count = count_people_yolo(frame)

    # ---------- FUSION ----------
    if csr_count < 15:
        final_count = max(csr_count * SPARSE_CALIBRATION, yolo_count)
    elif csr_count < 60:
        final_count = 0.5 * (csr_count * SPARSE_CALIBRATION) + 0.5 * yolo_count
    else:
        final_count = min(csr_count, yolo_count * 5)

    final_count = max(0, final_count)

    # ---------- VISUAL ----------
    if is_webcam:
        density_vis = cv2.GaussianBlur(density, (31, 31), 0)
    else:
        density_vis = cv2.GaussianBlur(density, (15, 15), 0)

    max_val = density_vis.max()
    density_norm = density_vis / max_val if max_val > 0 else density_vis
    density_norm = np.clip(density_norm, 0, 1)

    heatmap = np.uint8(255 * density_norm)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]))

    overlay = cv2.addWeighted(frame, 0.6, heatmap, 0.4, 0)

    return frame, heatmap, overlay, final_count
