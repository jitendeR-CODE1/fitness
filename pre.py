import streamlit as st
import cv2
import numpy as np
from PIL import Image

def get_diet_plan(bmi, diet_type, meal_time):
    bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 24.9 else "Overweight"
    
    diet_plans = {
        "Underweight": {
            "Veg": {"Breakfast": "Oats, banana, nuts, and milk", "Lunch": "Lentils, rice, and mixed vegetables", "Snacks": "Dry fruits, banana shake", "Dinner": "Dal, roti, and vegetable stir fry"},
            "Non-Veg": {"Breakfast": "Eggs, toast, and milk", "Lunch": "Chicken, rice, and salad", "Snacks": "Boiled eggs and nuts", "Dinner": "Grilled chicken with rice"},
            "Semi-Veg": {"Breakfast": "Oats, eggs, and fruit", "Lunch": "Fish, quinoa, and vegetables", "Snacks": "Cheese toast with peanut butter", "Dinner": "Fish with steamed veggies"}
        },
        "Normal": {
            "Veg": {"Breakfast": "Whole wheat toast, peanut butter, and smoothie", "Lunch": "Paneer curry with whole wheat roti", "Snacks": "Fruit bowl with honey", "Dinner": "Quinoa salad with chickpeas"},
            "Non-Veg": {"Breakfast": "Boiled eggs, toast, and coffee", "Lunch": "Grilled chicken with brown rice", "Snacks": "Tuna sandwich", "Dinner": "Grilled salmon with greens"},
            "Semi-Veg": {"Breakfast": "Scrambled eggs, fruit, and yogurt", "Lunch": "Fish curry with brown rice", "Snacks": "Greek yogurt with almonds", "Dinner": "Egg curry with chapati"}
        },
        "Overweight": {
            "Veg": {"Breakfast": "Smoothie with spinach, banana, and protein powder", "Lunch": "Salad with chickpeas and olive oil", "Snacks": "Carrot and cucumber sticks with hummus", "Dinner": "Soup with whole wheat bread"},
            "Non-Veg": {"Breakfast": "Omelet with veggies and green tea", "Lunch": "Grilled fish with quinoa", "Snacks": "Boiled eggs with nuts", "Dinner": "Grilled turkey with vegetables"},
            "Semi-Veg": {"Breakfast": "Greek yogurt with nuts and berries", "Lunch": "Egg salad with mixed greens", "Snacks": "Protein shake with fruits", "Dinner": "Baked fish with asparagus"}
        }
    }
    return diet_plans[bmi_category][diet_type][meal_time]

def get_exercise_plan(goal, body_type, injury):
    if goal == "Weight Loss":
        plan = "Cardio exercises like running, cycling, and HIIT workouts. Strength training 3-4 times a week."
        rest = "Rest for 30-45 seconds between sets."
    elif goal == "Muscle Gain":
        plan = "Strength training 5 times a week focusing on progressive overload. Compound movements like squats, deadlifts, and bench presses."
        rest = "Rest for 60-90 seconds between sets."
    else:  # Endurance
        plan = "Full-body functional workouts including circuit training, swimming, and endurance-focused exercises."
        rest = "Rest for 45-60 seconds between exercises."
    
    if injury:
        plan += f"\n*Special consideration for injury: {injury}. Please consult a professional trainer before proceeding.*"
    
    return plan, rest

def generate_weekly_report(diet_data, exercise_data):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    report = ""
    
    for day in days:
        report += f"## {day}\n"
        report += "### Diet Plan\n"
        report += f"- **Breakfast**: {diet_data['Breakfast']}\n"
        report += f"- **Lunch**: {diet_data['Lunch']}\n"
        report += f"- **Snacks**: {diet_data['Snacks']}\n"
        report += f"- **Dinner**: {diet_data['Dinner']}\n"
        report += "### Exercise Plan\n"
        report += f"- {exercise_data['plan']}\n"
        report += f"- **Rest Duration**: {exercise_data['rest']}\n\n"
    
    return report

def main():
    st.set_page_config(page_title="AI Fitness Coach", layout="wide")
    
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "diet_data" not in st.session_state:
        st.session_state.diet_data = {}
    if "exercise_data" not in st.session_state:
        st.session_state.exercise_data = {}

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
            
            # Store diet plan in session state
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
            
            # Store exercise plan in session state
            st.session_state.exercise_data = {"plan": plan, "rest": rest}
            st.success("Exercise plan saved!")
    
    elif st.session_state.page == "Generate Report":
        st.title("Generate Weekly Report")
        st.write("Generate a weekly report based on your diet and exercise plans.")
        
        if st.session_state.diet_data and st.session_state.exercise_data:
            if len(st.session_state.diet_data) == 4:  # Check if all meal times are filled
                report = generate_weekly_report(st.session_state.diet_data, st.session_state.exercise_data)
                st.write("### Your Weekly Fitness Report")
                st.markdown(report)
                
                # Option to download the report as a text file
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

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> c9f6d73 (Fixed indentation issues in Exercise modules)
