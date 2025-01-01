import streamlit as st
from PIL import Image
import os
import pandas as pd

# Set page config
st.set_page_config(page_title="ImpactHub", layout="wide")

# Apply custom CSS for the moving title and styling
st.markdown("""
    <style>
    @keyframes moveText {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .moving-title {
        overflow: hidden;
        white-space: nowrap;
    }
    
    .moving-title h1 {
        display: inline-block;
        animation: moveText 15s linear infinite;
        color: red;
        font-size: 4em;
        font-weight: bold;
    }
    
    .card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 0.5rem;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .sidebar-nav {
        padding: 1rem;
    }
    
    .stButton>button {
        width: 100%;
        margin: 0.2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

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
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    # Weekly tabs
    st.subheader("Weekly Assignments")
    for i in range(1, 16):
        if st.button(f"Week {i}"):
            st.session_state.current_page = f"Week {i}"
    
    # Quiz tabs
    st.subheader("Quizzes")
    for i in range(1, 11):
        if st.button(f"Quiz {i}"):
            st.session_state.current_page = f"Quiz {i}"
    
    st.markdown('</div>', unsafe_allow_html=True)

# Function to create a card
def create_card(title, description="Click to view details"):
    card_html = f"""
        <div class="card" onclick="window.location.href='#{title.lower().replace(' ', '')}'">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

# Main content area - Weekly Assignments
st.subheader("Weekly Assignments")
for i in range(1, 16, 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j <= 15:
            with cols[j]:
                create_card(f"Week {i + j}")

# Main content area - Quizzes
st.subheader("Quizzes")
for i in range(1, 11, 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j <= 10:
            with cols[j]:
                create_card(f"Quiz {i + j}")
