def detect_situps(keypoints, state, reps, threshold=50):
     if keypoints is None or len(keypoints) < 12:
        return "No detection", reps, state
    r_hip = keypoints[11]
    r_shoulder = keypoints[5]
    r_elbow = keypoints[7]

    angle = calculate_angle(r_hip, r_shoulder, r_elbow)

    if angle < 90:
        if r_shoulder[1] < r_hip[1] - threshold and state == "down":
            state = "up"
            reps += 1
        elif r_shoulder[1] > r_hip[1] and state == "up":
            state = "down"
    return "Sit-ups", reps, state
