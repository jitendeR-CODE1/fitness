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

       if __name__ == "__main__":
              main()