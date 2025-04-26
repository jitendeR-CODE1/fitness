import streamlit as st
import cv2
import time
import numpy as np
from ultralytics import YOLO
import math

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Pushup Counter App
def detect():
    st.title('Pushup Counter')

    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])
    if uploaded_file is not None:
        tfile = open('temp.mp4', 'wb')
        tfile.write(uploaded_file.read())
        tfile.close()

        cap = cv2.VideoCapture('temp.mp4')

        model = YOLO('yolov8n-pose.pt')

        counter = 0
        stage = None

        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            results = model(frame, show=False)
            keypoints = results[0].keypoints.xy.cpu().numpy()

            if keypoints.size != 0:
                left_shoulder = keypoints[0][5]
                left_elbow = keypoints[0][7]
                left_wrist = keypoints[0][9]

                angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                if angle > 160:
                    stage = "up"
                if angle < 90 and stage == 'up':
                    stage = "down"
                    counter += 1

                cv2.putText(frame, str(counter),
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame, channels="RGB", use_column_width=True)

        cap.release()
