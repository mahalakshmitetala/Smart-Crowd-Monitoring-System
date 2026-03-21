import smtplib
from email.message import EmailMessage
from datetime import datetime
import cv2

SENDER_EMAIL = "mahalakshmitetala0909@gmail.com"
APP_PASSWORD = "kqujqjdyyryccoaj"


def send_alert(to_email, count, density_img):

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # save density screenshot
    filename = "density_alert.jpg"
    cv2.imwrite(filename, density_img)

    msg = EmailMessage()
    msg["Subject"] = "🚨 Crowd Density Alert"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    msg.set_content(f"""
Crowd Alert Detected

Date: {date_str}
Time: {time_str}
Estimated Crowd Count: {int(count)}

See attached density map.
""")

    with open(filename, "rb") as f:
        img_data = f.read()

    msg.add_attachment(
        img_data,
        maintype="image",
        subtype="jpeg",
        filename="density_map.jpg"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)