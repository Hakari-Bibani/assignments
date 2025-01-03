import streamlit as st

def apply_style():
    """Apply custom styling to the Streamlit app"""
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Moving title animation */
        @keyframes moveText {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .moving-title {
            overflow: hidden;
            white-space: nowrap;
            margin-bottom: 2rem;
        }

        .moving-title h1 {
            display: inline-block;
            color: #FF0000;
            font-size: 3.5rem;
            font-weight: bold;
            animation: moveText 15s linear infinite;
        }

        /* Flip card styling */
        .stCard {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        .stCard:hover {
            transform: scale(1.05);
        }

        /* Navigation sidebar styling */
        .css-1d391kg {
            background-color: #f0f2f6;
        }

        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }

        /* Header styling */
        h1 {
            font-family: 'Arial Black', sans-serif;
            color: #1E1E1E;
            margin-bottom: 2rem;
        }

        h2 {
            font-family: 'Arial', sans-serif;
            color: #2E2E2E;
            margin-bottom: 1.5rem;
        }

        /* Custom styling for radio buttons */
        .stRadio > label {
            font-weight: bold;
            color: #2E2E2E;
        }

        /* Card content styling */
        .card-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #1E1E1E;
        }

        .card-text {
            font-size: 0.9rem;
            color: #666;
        }
        </style>
    """, unsafe_allow_html=True)
