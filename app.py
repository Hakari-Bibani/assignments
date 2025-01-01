import streamlit as st
from PIL import Image
import os
import pandas as pd
from st_pages import Page, show_pages, add_page_title
from streamlit_card import card
import style

# Set page config
st.set_page_config(page_title="ImpactHub", layout="wide")

# Apply custom styles
style.apply_styles()

# Create animated title
st.markdown("""
    <div class="moving-title">
        <h1>ImpactHub</h1>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    tabs = ["Week " + str(i) for i in range(1, 16)] + ["Quiz " + str(i) for i in range(1, 11)]
    for tab in tabs:
        if st.button(tab):
            st.session_state.current_page = tab

# Main content area
def create_card(title, key):
    return card(
        title=title,
        text="Click to view details",
        key=key,
    )

# Create grid layout for cards
col1, col2, col3 = st.columns(3)

# Weekly assignments cards
with st.container():
    st.subheader("Weekly Assignments")
    for i in range(1, 16, 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            if i <= 15:
                create_card(f"Week {i}", f"week_{i}")
        with col2:
            if i + 1 <= 15:
                create_card(f"Week {i+1}", f"week_{i+1}")
        with col3:
            if i + 2 <= 15:
                create_card(f"Week {i+2}", f"week_{i+2}")

# Quiz cards
with st.container():
    st.subheader("Quizzes")
    for i in range(1, 11, 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            if i <= 10:
                create_card(f"Quiz {i}", f"quiz_{i}")
        with col2:
            if i + 1 <= 10:
                create_card(f"Quiz {i+1}", f"quiz_{i+1}")
        with col3:
            if i + 2 <= 10:
                create_card(f"Quiz {i+2}", f"quiz_{i+2}")
