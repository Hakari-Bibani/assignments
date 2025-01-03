import pandas as pd
from geopy.distance import geodesic

# Coordinates
coordinates = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# Calculate distances between points
def calculate_distances(coords):
    point1, point2, point3 = coords
    dist1_2 = geodesic(point1, point2).kilometers
    dist2_3 = geodesic(point2, point3).kilometers
    dist1_3 = geodesic(point1, point3).kilometers
    return dist1_2, dist2_3, dist1_3

# Grade submission
def grade_submission(student_code):
    try:
        exec_globals = {}
        exec(student_code, exec_globals)
        distances = calculate_distances(coordinates)

        score = 0
        if isinstance(distances, tuple) and len(distances) == 3:
            score += 30  # Placeholder for detailed grading logic
        return score
    except Exception as e:
        return f"Error in grading: {e}"

# Example usage
if __name__ == "__main__":
    try:
        submissions = pd.read_csv("grades/data_submission.csv")
        submissions["Grade"] = submissions["Assignment 1"].apply(grade_submission)
        submissions.to_csv("grades/data_submission.csv", index=False)
        print("Grading completed.")
    except FileNotFoundError:
        print("No submissions found.")
