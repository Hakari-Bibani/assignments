import streamlit as st

def page_config():
    # Configure the page
    st.set_page_config(
        page_title="ImpactHub",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS
    st.markdown("""
        <style>
        /* Main content styling */
        .stButton button {
            background-color: #f0f2f6;
            border: 2px solid #4CAF50;
            color: black;
            padding: 10px 24px;
            margin: 5px 0;
            cursor: pointer;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #4CAF50;
            color: white;
            transform: scale(1.02);
        }
        
        /* Header styling */
        h1 {
            color: #ff0000;
            text-align: center;
            padding: 20px;
            font-family: 'Arial Black', sans-serif;
        }
        
        h2 {
            color: #2c3e50;
            font-family: 'Arial', sans-serif;
            margin-bottom: 20px;
        }
        
        /* Error message styling */
        .stError {
            background-color: #ffebee;
            padding: 10px;
            border-radius: 5px;
            border-left: 5px solid #ff5252;
        }
        </style>
    """, unsafe_allow_html=True)
