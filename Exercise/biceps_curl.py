import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import math

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def run():
    st.title('Bicep Curl Counter')

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
                shoulder = keypoints[0][5]
                elbow = keypoints[0][7]
                wrist = keypoints[0][9]

                angle = calculate_angle(shoulder, elbow, wrist)

                if angle > 160:
                    stage = "down"
                if angle < 45 and stage == 'down':
                    stage = "up"
                    counter += 1

                cv2.putText(frame, str(counter),
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame, channels="RGB", use_column_width=True)

        cap.release()
