import streamlit as st
import pandas as pd
import os
from grades.grade1 import calculate_grade
from streamlit_folium import folium_static  # For displaying folium maps
import re  # For extracting distances from print statements

# Ensure the grades directory exists
if not os.path.exists("grades"):
    os.makedirs("grades")

# Streamlit app title
st.title("Week 1 Assignment: Mapping Coordinates and Calculating Distances")

# Student information input
st.header("Student Information")
full_name = st.text_input("Full Name")
email = st.text_input("Email")
student_id = st.text_input("Student ID")

# Assignment details
st.header("Assignment Details")
with st.expander("View Assignment Instructions"):
    st.markdown("""
    **Assignment: Week 1 – Mapping Coordinates and Calculating Distances in Python**

    **Objective:**  
    In this assignment, you will write a Python script to plot three geographical coordinates on a map and calculate the distance between each pair of points in kilometers.

    **Task Requirements:**
    1. **Plot the Three Coordinates on a Map:**
       - Use Python libraries to plot the points on a map.
       - The map should visually display the exact locations of the coordinates.
    2. **Calculate the Distance Between Each Pair of Points:**
       - Calculate the distances between the three points in **kilometers**.

    **Coordinates:**
    - **Point 1:** Latitude: 36.325735, Longitude: 43.928414
    - **Point 2:** Latitude: 36.393432, Longitude: 44.586781
    - **Point 3:** Latitude: 36.660477, Longitude: 43.840174

    **Python Libraries You Will Use:**
    - **geopy** for calculating distances.
    - **folium** for plotting points on an interactive map.
    - **geopandas** (optional) for advanced map rendering.

    **Expected Output:**
    1. A **map** showing the three coordinates.
    2. A **text summary** showing the calculated distances (in kilometers) between:
       - Point 1 and Point 2.
       - Point 2 and Point 3.
       - Point 1 and Point 3.
    """)

# Code submission
st.header("Code Submission")
student_code = st.text_area("Paste your Python code here", height=300)

# Run Code button
if st.button("Run Code"):
    if not student_code.strip():
        st.error("Please paste your code before running.")
    else:
        try:
            # Redirect print statements to capture distances
            from io import StringIO
            import sys
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            # Execute the student's code in a new namespace
            namespace = {}
            exec(student_code, namespace)

            # Restore stdout and capture printed output
            printed_output = sys.stdout.getvalue()
            sys.stdout = old_stdout

            st.success("Code executed successfully!")

            # Display the map if it exists
            if 'map' in namespace:
                st.header("Map Visualization")
                folium_static(namespace['map'])  # Display the folium map
            else:
                st.warning("No map found in the output. Ensure your code generates a 'map' variable using folium.")

            # Extract distances from printed output
            distances = {}
            distance_pattern = r"Point \d to Point \d: (\d+\.\d+) km"
            matches = re.findall(distance_pattern, printed_output)
            if matches:
                distances = {
                    "Point 1 to Point 2": float(matches[0]),
                    "Point 2 to Point 3": float(matches[1]),
                    "Point 1 to Point 3": float(matches[2])
                }

            # Display the distance report if it exists
            if distances:
                st.header("Distance Report")
                st.write(distances)
            else:
                st.warning("No distance report found in the output. Ensure your code prints the distances in the format: 'Point X to Point Y: Z km'.")
        except ModuleNotFoundError as e:
            if "IPython" in str(e):
                st.error("Error: The 'IPython' library is not supported in this environment. Please remove any 'IPython' dependencies from your code.")
            else:
                st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"Error executing code: {e}")

# Submit Assignment button
if st.button("Submit Assignment"):
    if not full_name or not email or not student_id:
        st.error("Please fill in all student information fields.")
    elif not student_code.strip():
        st.error("Please paste your code before submitting.")
    else:
        # Calculate the grade
        grade = calculate_grade(student_code)

        # Save the grade and student information
        data = {
            "Full name": [full_name],
            "Email": [email],
            "Student ID": [student_id],
            "assignment1": [grade],
            "total": [grade]  # Assuming this is the first assignment
        }
        df = pd.DataFrame(data)

        # Append to the CSV file
        if not os.path.exists("grades/data_submission.csv"):
            df.to_csv("grades/data_submission.csv", index=False)
        else:
            existing_df = pd.read_csv("grades/data_submission.csv")
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv("grades/data_submission.csv", index=False)

        st.success(f"Assignment submitted successfully! Your grade is: {grade}/100")
