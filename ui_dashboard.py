import os

# Fix OpenCV issue on Streamlit Cloud
os.system("pip uninstall -y opencv-python opencv-python-headless")
os.system("pip install opencv-python-headless==4.8.1.78")
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

from density_core import run_density
from alert_db import init_db, add_email, get_emails
from alert_mailer import send_alert

# ---------------- INIT ----------------
init_db()

st.set_page_config(
    page_title="Smart Crowd Monitoring System",
    layout="wide"
)

st.title("🚦 Smart Crowd Monitoring System")

# ---------------- SESSION STATE ----------------
if "video_done" not in st.session_state:
    st.session_state.video_done = False

if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = 0

ALERT_COOLDOWN = 15

# ---------------- SIDEBAR ----------------
st.sidebar.header("📧 Alert Emails")

email = st.sidebar.text_input("Add Email")

if st.sidebar.button("Save Email"):
    if email:
        add_email(email)
        st.sidebar.success("Email added")

# ---------------- CONTROLS ----------------
input_mode = st.radio(
    "Select Input Source",
    ["Live Webcam", "Video File"]
)

threshold = st.slider("Alert Threshold", 1, 300, 10)

# ---------------- DISPLAY AREAS ----------------
col1, col2, col3 = st.columns(3)

orig_box = col1.empty()
dens_box = col2.empty()
over_box = col3.empty()

count_box = st.empty()
alert_box = st.empty()

# ================= VIDEO MODE =====================

if input_mode == "Video File":

    uploaded = st.file_uploader("Upload Video", ["mp4", "avi", "mov"])

    if uploaded:
        st.session_state.video_done = False

        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded.read())

    if uploaded and not st.session_state.video_done:

        cap = cv2.VideoCapture("temp_video.mp4")

        while True:
            ret, frame = cap.read()

            if not ret:
                cap.release()
                st.session_state.video_done = True
                st.success("✅ Video processing completed")
                break

            o, d, ov, count = run_density(frame, is_webcam=False)

            orig_box.image(o, channels="BGR")
            dens_box.image(d, channels="BGR")
            over_box.image(ov, channels="BGR")

            count_box.metric("👥 Crowd Count", int(round(count)))

            # -------- ALERT ----------
            if count > threshold:
                alert_box.error("⚠️ CROWD ALERT")

                current_time = time.time()

                if current_time - st.session_state.last_alert_time > ALERT_COOLDOWN:
                    st.session_state.last_alert_time = current_time

                    for e in get_emails():
                        try:
                            send_alert(e, count, ov)
                        except Exception as ex:
                            st.error(f"Email error: {ex}")
            else:
                alert_box.success("SAFE")

            time.sleep(0.03)  # 🔥 prevents overload (IMPORTANT)

# ================= WEBCAM MODE ====================

if input_mode == "Live Webcam":

    camera = st.camera_input("Use Webcam")

    if camera is not None:

        image = Image.open(camera)
        frame = np.array(image)

        o, d, ov, count = run_density(frame, is_webcam=True)

        orig_box.image(o, channels="BGR")
        dens_box.image(d, channels="BGR")
        over_box.image(ov, channels="BGR")

        count_box.metric("👥 Crowd Count", int(round(count)))

        # -------- ALERT ----------
        if count > threshold:
            alert_box.error("⚠️ CROWD ALERT")

            current_time = time.time()

            if current_time - st.session_state.last_alert_time > ALERT_COOLDOWN:
                st.session_state.last_alert_time = current_time

                for e in get_emails():
                    try:
                        send_alert(e, count, ov)
                    except Exception as ex:
                        st.error(f"Email error: {ex}")
        else:
            alert_box.success("SAFE")
