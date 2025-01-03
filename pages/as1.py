import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
import os
import json
from datetime import datetime

# Constants
COORDINATES = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

EXPECTED_DISTANCES = {
    "1-2": geodesic(COORDINATES[0], COORDINATES[1]).kilometers,
    "2-3": geodesic(COORDINATES[1], COORDINATES[2]).kilometers,
    "1-3": geodesic(COORDINATES[0], COORDINATES[2]).kilometers
}

def calculate_distances(coords):
    """Calculate distances between points with error handling."""
    try:
        point1, point2, point3 = coords
        dist1_2 = geodesic(point1, point2).kilometers
        dist2_3 = geodesic(point2, point3).kilometers
        dist1_3 = geodesic(point1, point3).kilometers
        return dist1_2, dist2_3, dist1_3
    except Exception as e:
        st.error(f"Error calculating distances: {str(e)}")
        return None

def create_map_with_popups(coords):
    """Create an interactive map with enhanced features."""
    try:
        # Center the map based on the average coordinates
        center_lat = sum(coord[0] for coord in coords) / len(coords)
        center_lon = sum(coord[1] for coord in coords) / len(coords)
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=9,
            tiles="cartodbpositron"
        )

        # Calculate distances
        distances = calculate_distances(coords)
        if not distances:
            return None
        
        dist1_2, dist2_3, dist1_3 = distances

        # Add markers with enhanced popups
        colors = ["blue", "green", "red"]
        for i, (coord, color) in enumerate(zip(coords, colors)):
            popup_content = f"""
            <div style='font-family: Arial; font-size: 12px;'>
                <b>Point {i+1}</b><br>
                Latitude: {coord[0]:.6f}<br>
                Longitude: {coord[1]:.6f}<br>
                <hr style='margin: 5px 0;'>
                Distances:<br>
            """
            if i == 0:
                popup_content += f"To Point 2: {dist1_2:.2f} km<br>To Point 3: {dist1_3:.2f} km"
            elif i == 1:
                popup_content += f"To Point 1: {dist1_2:.2f} km<br>To Point 3: {dist2_3:.2f} km"
            else:
                popup_content += f"To Point 1: {dist1_3:.2f} km<br>To Point 2: {dist2_3:.2f} km"
            popup_content += "</div>"

            folium.Marker(
                location=coord,
                popup=folium.Popup(popup_content, max_width=200),
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(m)

        # Add polylines with distance labels
        for i in range(len(coords)):
            j = (i + 1) % len(coords)
            midpoint = [
                (coords[i][0] + coords[j][0]) / 2,
                (coords[i][1] + coords[j][1]) / 2
            ]
            distance = geodesic(coords[i], coords[j]).kilometers
            
            # Add line
            folium.PolyLine(
                locations=[coords[i], coords[j]],
                color="blue",
                weight=2,
                opacity=0.8,
                dash_array="5, 10"
            ).add_to(m)
            
            # Add distance label
            folium.Popup(
                f"{distance:.2f} km",
                permanent=True
            ).add_to(folium.CircleMarker(
                location=midpoint,
                radius=1,
                color="black",
                fill=True
            ).add_to(m))

        return m
    except Exception as e:
        st.error(f"Error creating map: {str(e)}")
        return None

def grade_submission(user_distances, expected_distances):
    """Grade the submission based on distance calculations."""
    try:
        if not user_distances:
            return 0
        
        total_score = 0
        tolerance = 0.1  # 100 meter tolerance
        
        # Compare each distance with expected values
        dist1_2, dist2_3, dist1_3 = user_distances
        expected_values = [
            expected_distances["1-2"],
            expected_distances["2-3"],
            expected_distances["1-3"]
        ]
        
        for user_dist, expected_dist in zip(user_distances, expected_values):
            if abs(user_dist - expected_dist) <= tolerance:
                total_score += 33.33
        
        return min(round(total_score), 100)
    except Exception as e:
        st.error(f"Error grading submission: {str(e)}")
        return 0

def save_submission(data):
    """Save submission data with error handling."""
    try:
        # Ensure the grades directory exists
        os.makedirs("grades", exist_ok=True)
        
        filepath = "grades/data_submission.csv"
        
        # Add timestamp to submission
        data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            df = pd.read_csv(filepath)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Full Name", "Student ID", "Email", "Assignment 1", "Total", "Timestamp"])
        
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(filepath, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving submission: {str(e)}")
        return False

def main():
    st.set_page_config(page_title="Assignment 1", layout="wide")
    
    # Title with custom styling
    st.markdown("""
        <h1 style='text-align: center; color: #1E88E5;'>
            Week 1 - Mapping Coordinates and Calculating Distances
        </h1>
        <hr>
    """, unsafe_allow_html=True)

    # Create two columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Student Information with validation
        with st.form("student_info"):
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            student_id = st.text_input("Student ID")
            submit_info = st.form_submit_button("Continue")

            if submit_info:
                if not name or not email:
                    st.error("Please fill in all required fields (*)")
                    return
                if "@" not in email:
                    st.error("Please enter a valid email address")
                    return

    with col2:
        # Assignment Details
        with st.expander("📝 Assignment Details", expanded=True):
            st.markdown("""
                ### Objective
                Plot three geographical coordinates on a map and calculate distances between them.
                
                ### Points
                1. Point 1: (36.325735, 43.928414)
                2. Point 2: (36.393432, 44.586781)
                3. Point 3: (36.660477, 43.840174)
                
                ### Required Output
                - Interactive map with markers
                - Distance calculations between points
            """)

    # Code Input with syntax highlighting
    st.markdown("### 💻 Your Code")
    code = st.text_area(
        "Paste your Python code here:",
        height=200,
        help="Write or paste your Python code that implements the required functionality"
    )

    # Tabbed Interface
    tab1, tab2 = st.tabs(["▶️ Run Code", "📤 Submit"])

    with tab1:
        if st.button("Execute Code", type="primary"):
            with st.spinner("Running your code..."):
                distances = calculate_distances(COORDINATES)
                if distances:
                    map_obj = create_map_with_popups(COORDINATES)
                    if map_obj:
                        st_folium(map_obj, width=800, height=600, returned_objects=[])
                        
                        st.markdown("### 📊 Distance Report")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Points 1-2", f"{distances[0]:.2f} km")
                        with col2:
                            st.metric("Points 2-3", f"{distances[1]:.2f} km")
                        with col3:
                            st.metric("Points 1-3", f"{distances[2]:.2f} km")

    with tab2:
        if st.button("Submit Assignment", type="primary"):
            if not name or not email:
                st.error("Please fill in your information first")
                return
            
            distances = calculate_distances(COORDINATES)
            if distances:
                score = grade_submission(distances, EXPECTED_DISTANCES)
                
                submission_data = {
                    "Full Name": name,
                    "Student ID": student_id,
                    "Email": email,
                    "Assignment 1": score,
                    "Total": score
                }
                
                if save_submission(submission_data):
                    st.success(f"✅ Submission successful! Score: {score}/100")
                    st.balloons()
                else:
                    st.error("Failed to save submission. Please try again.")

if __name__ == "__main__":
    main()
