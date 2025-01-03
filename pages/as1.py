# pages/as1.py
import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium

# Coordinates
coordinates = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# Function to create map
def create_map(coords):
    m = folium.Map(location=[36.5, 44], zoom_start=9)
    
    # Add markers
    for i, coord in enumerate(coords, 1):
        folium.Marker(
            coord,
            popup=f'Point {i}',
            icon=folium.Icon(color='red')
        ).add_to(m)
    
    # Add lines connecting points
    folium.PolyLine(
        coords,
        color="blue",
        weight=2,
        opacity=0.8
    ).add_to(m)
    
    return m

# Function to calculate distances
def calculate_distances(coords):
    dist1_2 = geodesic(coords[0], coords[1]).kilometers
    dist2_3 = geodesic(coords[1], coords[2]).kilometers
    dist1_3 = geodesic(coords[0], coords[2]).kilometers
    return dist1_2, dist2_3, dist1_3

# Streamlit UI
st.title("Week 1 - Mapping Coordinates and Calculating Distances")

# Student Information
name = st.text_input("Full Name")
email = st.text_input("Email")
student_id = st.text_input("Student ID (Optional)")

# Assignment Details
with st.expander("Assignment Details"):
    st.write(
        "Plot three geographical coordinates on a map and calculate distances between them."
    )

# Code Input
code = st.text_area("Paste your Python code here:", height=200)

# Tabs
tab1, tab2 = st.tabs(["Run Code", "Submit"])

# Run Code Tab
with tab1:
    if st.button("Run Code"):
        try:
            # Create map
            m = create_map(coordinates)
            
            # Display map
            st_folium(m, width=800)
            
            # Calculate and display distances
            distances = calculate_distances(coordinates)
            
            st.write("### Distance Calculations:")
            st.write(f"Distance between Point 1 and Point 2: {distances[0]:.2f} km")
            st.write(f"Distance between Point 2 and Point 3: {distances[1]:.2f} km")
            st.write(f"Distance between Point 1 and Point 3: {distances[2]:.2f} km")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Submit Tab
with tab2:
    if st.button("Submit"):
        if not name or not email:
            st.error("Name and Email are required to submit.")
        else:
            # Save submission
            try:
                new_entry = {
                    "Full Name": name,
                    "Student ID": student_id,
                    "Assignment 1": 100,  # Placeholder score
                    "Total": 100
                }
                
                try:
                    df = pd.read_csv("grades/data_submission.csv")
                except FileNotFoundError:
                    df = pd.DataFrame(columns=["Full Name", "Student ID", "Assignment 1", "Total"])
                
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                df.to_csv("grades/data_submission.csv", index=False)
                st.success("Submission successful!")
            except Exception as e:
                st.error(f"Error saving submission: {str(e)}")
