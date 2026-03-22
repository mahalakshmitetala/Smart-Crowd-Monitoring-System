# Smart-Crowd-Monitoring-System
AI-based crowd density monitoring system for real-time crowd analysis using webcam or uploaded videos. The system generates density maps, estimates crowd count, and sends automated email alerts with screenshot evidence when crowd exceeds a configurable threshold.

## Features
- Real-time crowd density estimation
- Webcam and video file input support
- Density map and overlay visualization
- Crowd count estimation
- Threshold-based alert detection
- Automated email alerts with screenshot attachment
- Streamlit-based interactive dashboard

### Dashboard
![Dashboard](dashboard.png)

### videoframe Mode
![Video Output](videoframes_output.png)

### Crowd Alert Detection
![Alert](email_alert.png)

## Technologies Used

- Python
- Streamlit
- OpenCV
- PyTorch
- Deep Learning (CSRNet)
- NumPy

## Application Use Cases

- Crowd monitoring in public events
- Railway stations and bus terminals
- Religious gatherings
- Stadiums and concerts
- Smart city surveillance
- Stampede risk prevention

 ## Future Scope

This system can be further enhanced by integrating support for multiple camera feeds to enable large-scale crowd monitoring across different locations simultaneously. Mobile-based notifications such as SMS or push alerts can also be added to ensure faster communication during overcrowding situations. Additionally, zone-based crowd analysis can be implemented to monitor specific high-risk areas and trigger localized alerts. The model accuracy can be further improved by training on larger and more diverse datasets and by experimenting with advanced deep learning architectures, which would improve reliability and make the system more suitable for real-world deployments.
