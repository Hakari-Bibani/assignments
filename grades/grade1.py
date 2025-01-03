def grade_assignment(student_code):
    # Execute student code and capture output
    try:
        exec(student_code)
        # Check if map is generated
        if "map.html" in os.listdir():
            map_score = 40  # Full marks for map
        else:
            map_score = 0

        # Check distance calculations
        distance_score = 0
        if abs(distance_1_2 - 59.12) < 1:  # Approximate expected distance
            distance_score += 20
        if abs(distance_2_3 - 74.34) < 1:
            distance_score += 20
        if abs(distance_1_3 - 37.45) < 1:
            distance_score += 20

        total_score = map_score + distance_score
        return total_score
    except Exception as e:
        print(f"Error in student code: {e}")
        return 0
