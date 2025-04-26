import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import time
import base64
import importlib
from pathlib import Path

from pre import get_diet_plan, get_exercise_plan, generate_weekly_report

# Load YOLOv11 model
@st.cache_resource
def load_model():
    return YOLO("yolo11n-pose.pt")

def play_audio():
    if Path("beep.wav").exists():
        audio_bytes = Path("beep.wav").read_bytes()
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="AI Fitness Coach", layout="wide")

    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "diet_data" not in st.session_state:
        st.session_state.diet_data = {}
    if "exercise_data" not in st.session_state:
        st.session_state.exercise_data = {}
    if "reps" not in st.session_state:
        st.session_state.reps = 0
    if "state" not in st.session_state:
        st.session_state.state = "up"

    with st.sidebar:
        st.title("AI Fitness Coach")
        option = st.radio(" ", ["Home", "Diet Planner", "Tutorials", "Real-Time Monitoring", "Exercise Planner", "Generate Report"],
                          index=["Home", "Diet Planner", "Tutorials", "Real-Time Monitoring", "Exercise Planner", "Generate Report"].index(st.session_state.page))

        if option != st.session_state.page:
            st.session_state.page = option
            st.rerun()

    if st.session_state.page == "Home":
        st.title("Welcome to Your AI Fitness Coach")
        st.write("\"Your only limit is you. Push yourself because no one else is going to do it for you.\"")
        if st.button("Start Training"):
            st.session_state.page = "Diet Planner"
            st.rerun()

    elif st.session_state.page == "Diet Planner":
        st.title("Diet Planner")
        st.write("Plan your diet according to your fitness goals.")

        weight = st.number_input("Enter your weight (kg)", min_value=30.0, max_value=200.0, step=0.1)
        height = st.number_input("Enter your height (cm)", min_value=100.0, max_value=250.0, step=0.1)

        if weight and height:
            bmi = weight / ((height / 100) ** 2)
            st.write(f"Your BMI: {bmi:.2f}")

            diet_type = st.selectbox("Select your diet preference", ["Veg", "Non-Veg", "Semi-Veg"])
            meal_time = st.radio("Select Meal Time", ["Breakfast", "Lunch", "Snacks", "Dinner"])
            diet_plan = get_diet_plan(bmi, diet_type, meal_time)
            st.write("### Suggested Diet Plan:")
            st.write(diet_plan)

            if st.button("Save Diet Plan"):
                st.session_state.diet_data[meal_time] = diet_plan
                st.success(f"{meal_time} diet plan saved!")

    elif st.session_state.page == "Tutorials":
        st.title("Workout Tutorials")
        st.write("Search for a muscle group or an exercise.")

        muscle_groups = {
            "Legs": {
                "Squats": "https://www.youtube.com/embed/aclHkVaku9U",
                "Lunges": "https://www.youtube.com/embed/QOVaHwm-Q6U",
                "Leg Press": "https://www.youtube.com/embed/IZxyjW7MPJQ"
            },
            "Biceps": {
                "Bicep Curls": "https://www.youtube.com/embed/ykJmrZ5v0Oo",
                "Hammer Curls": "https://www.youtube.com/embed/zC3nLlEvin4",
                "Preacher Curls": "https://www.youtube.com/embed/wgSHaPZWe5o"
            },
            "Triceps": {
                "Tricep Dips": "https://www.youtube.com/embed/0326dy_-CzM",
                "Skull Crushers": "https://www.youtube.com/embed/d_KZxkY_0cM",
                "Close-Grip Bench Press": "https://www.youtube.com/embed/6G3kQyq8yts"
            },
            "Shoulders": {
                "Shoulder Press": "https://www.youtube.com/embed/B-aVuyhvLHU",
                "Lateral Raises": "https://www.youtube.com/embed/3VcKaXpzqRo",
                "Front Raises": "https://www.youtube.com/embed/-t7fuZ0KhDA"
            }
        }

        search_query = st.text_input("Search for an exercise", "").lower()
        found_exercises = []

        for muscle, exercises in muscle_groups.items():
            for exercise, video_url in exercises.items():
                if search_query in exercise.lower() or search_query in muscle.lower():
                    found_exercises.append((exercise, video_url))

        if found_exercises:
            for exercise, video_url in found_exercises:
                st.subheader(exercise)
                st.video(video_url)
        else:
            st.write("No exercises found. Try searching for a different term.")

    elif st.session_state.page == "Exercise Planner":
        st.title("Personalized Exercise Planner")
        st.write("Get a workout plan based on your body type and fitness level.")

        height = st.number_input("Enter your height (cm)", min_value=100.0, max_value=250.0, step=0.1)
        weight = st.number_input("Enter your weight (kg)", min_value=30.0, max_value=200.0, step=0.1)
        body_type = st.selectbox("Select your body type", ["Endomorph", "Ectomorph", "Mesomorph"])
        goal = st.selectbox("Select your goal", ["Weight Loss", "Muscle Gain", "Endurance"])
        injury = st.text_area("Any past injuries? (Specify if applicable)")

        if st.button("Generate Plan"):
            plan, rest = get_exercise_plan(goal, body_type, injury)
            st.write(f"### Your Personalized Plan for {goal} ({body_type})")
            st.write(plan)
            st.write(f"### Recommended Rest Duration: {rest}")

            st.session_state.exercise_data = {"plan": plan, "rest": rest}
            st.success("Exercise plan saved!")

    elif st.session_state.page == "Generate Report":
        st.title("Generate Weekly Report")
        st.write("Generate a weekly report based on your diet and exercise plans.")

        if st.session_state.diet_data and st.session_state.exercise_data:
            if len(st.session_state.diet_data) == 4:
                report = generate_weekly_report(st.session_state.diet_data, st.session_state.exercise_data)
                st.write("### Your Weekly Fitness Report")
                st.markdown(report)

                st.download_button(
                    label="Download Report",
                    data=report,
                    file_name="weekly_fitness_report.txt",
                    mime="text/plain"
                )
            else:
                st.warning("Please save diet plans for all meal times (Breakfast, Lunch, Snacks, Dinner) in the Diet Planner.")
        else:
            st.warning("Please complete both the Diet Planner and Exercise Planner to generate a report.")

    elif st.session_state.page == "Real-Time Monitoring":
        st.title("📹 Real-Time Exercise Detection")

        exercise_options = sorted([f.stem for f in Path("Exercise").glob("*.py") if f.stem != "__init__"])
        selected_exercise = st.selectbox("Select Exercise to Monitor", exercise_options)

        if st.button("Reset Reps"):
            st.session_state.reps = 0
            st.session_state.state = "up"

        run = st.toggle("Start Webcam")

        FRAME_WINDOW = st.image([])

        if run:
            cap = cv2.VideoCapture(0)
            model = load_model()
            module = importlib.import_module(f"Exercise.{selected_exercise}")
            detect = module.detect

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                results = model(frame, verbose=False)
                annotated = frame.copy()

                for result in results:
                    if result.keypoints is not None:
                        keypoints = result.keypoints.xy[0].cpu().numpy()
                        label, reps, state = detect(keypoints, st.session_state.state, st.session_state.reps)

                        if reps > st.session_state.reps:
                            play_audio()

                        st.session_state.reps = reps
                        st.session_state.state = state
                        annotated = result.plot()

                cv2.putText(annotated, f"{selected_exercise} | Reps: {st.session_state.reps}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                FRAME_WINDOW.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
                time.sleep(0.03)

            cap.release()
        else:
            st.info("Camera is off.")

if __name__ == "__main__":
    main()
