# as1.py - Located in pages/as1.py
import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium

# Function to calculate distances between points
def calculate_distances(coords):
    point1, point2, point3 = coords
    dist1_2 = geodesic(point1, point2).kilometers
    dist2_3 = geodesic(point2, point3).kilometers
    dist1_3 = geodesic(point1, point3).kilometers
    return dist1_2, dist2_3, dist1_3

# Function to generate a folium map with popups showing distances
def create_map_with_popups(coords):
    # Initialize the map
    m = folium.Map(location=[36.5, 44], zoom_start=8, tiles="cartodbpositron")

    # Calculate distances
    dist1_2 = geodesic(coords[0], coords[1]).kilometers
    dist2_3 = geodesic(coords[1], coords[2]).kilometers
    dist1_3 = geodesic(coords[0], coords[2]).kilometers

    # Add markers with popups
    folium.Marker(
        location=coords[0],
        popup=f"Point 1<br>Distance to Point 2: {dist1_2:.2f} km<br>Distance to Point 3: {dist1_3:.2f} km",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    folium.Marker(
        location=coords[1],
        popup=f"Point 2<br>Distance to Point 1: {dist1_2:.2f} km<br>Distance to Point 3: {dist2_3:.2f} km",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(m)

    folium.Marker(
        location=coords[2],
        popup=f"Point 3<br>Distance to Point 1: {dist1_3:.2f} km<br>Distance to Point 2: {dist2_3:.2f} km",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Add a polyline to connect the points
    folium.PolyLine(
        locations=coords,
        color="blue",
        weight=3,
        opacity=0.8,
        tooltip="Path between points"
    ).add_to(m)

    return m

# Coordinates
coordinates = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# Streamlit UI
st.title("Week 1 - Mapping Coordinates and Calculating Distances")

# Student Information
name = st.text_input("Full Name")
email = st.text_input("Email")
student_id = st.text_input("Student ID (Optional)")

# Accordion for Assignment Details
with st.expander("Assignment Details"):
    st.write(
        "In this assignment, you will plot three geographical coordinates on a map "
        "and calculate distances between them. Paste your Python code below, run it, "
        "and submit your results."
    )

# Code Input
code = st.text_area("Paste your Python code here:", height=200)

# Tabbed UI
tabs = st.tabs(["Run Code", "Submit"])

# Tab: Run Code
with tabs[0]:
    if st.button("Run Code"):
        try:
            # Simulate user code execution
            distances = calculate_distances(coordinates)

            # Display Map
            map_obj = create_map_with_popups(coordinates)
            st_map = st_folium(map_obj, width=800, height=600, returned_objects=[])

            # Display Distances
            st.write("### Calculated Distances:")
            st.write(f"Distance between Point 1 and Point 2: {distances[0]:.2f} km")
            st.write(f"Distance between Point 2 and Point 3: {distances[1]:.2f} km")
            st.write(f"Distance between Point 1 and Point 3: {distances[2]:.2f} km")
        except Exception as e:
            st.error(f"Error in executing code: {e}")

# Tab: Submit
with tabs[1]:
    if st.button("Submit"):
        if not name or not email:
            st.error("Name and Email are required to submit.")
        else:
            distances = calculate_distances(coordinates)
            total_score = sum(distances)  # Placeholder for grading logic
            new_entry = {
                "Full Name": name,
                "Student ID": student_id,
                "Assignment 1": total_score,
                "Total": total_score
            }

            # Save to CSV
            try:
                df = pd.read_csv("grades/data_submission.csv")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["Full Name", "Student ID", "Assignment 1", "Total"])

            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv("grades/data_submission.csv", index=False)
            st.success("Submission successful!")
