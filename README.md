# Smart Crowd Monitoring System

AI-based real-time crowd density estimation using webcam or uploaded videos. Generates density heatmaps, estimates crowd count, and sends automated email alerts when crowd exceeds a set threshold.

🔗 **Live App:** [smart-crowd-monitoring-system.streamlit.app](https://smart-crowd-monitoring-system.streamlit.app)

---

## Features
- Real-time crowd density estimation (CSRNet + YOLO fusion)
- Webcam and video file input support
- Density heatmap and overlay visualization
- Configurable crowd threshold alerts
- Automated email alerts with screenshot attachment

## Tech Stack
- Python
- Streamlit
- OpenCV
- PyTorch
- CSRNet (Deep Learning)
- YOLOv8
- NumPy

## Use Cases
- Railway stations and bus terminals
- Religious gatherings
- Stadiums and concerts
- Smart city surveillance
- Stampede risk prevention

```markdown
## Model
- Architecture: CSRNet (Crowd counting via density estimation)
- Hosted on [Hugging Face](https://huggingface.co/mahaa2805/CSRNet_for_crowdmonitoring)
```
