import streamlit as st

def set_page_style():
    # Custom CSS styles
    st.markdown("""
        <style>
        /* Main container */
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Headers */
        .main-header {
            color: #1E88E5;
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 2rem;
        }
        
        /* Cards */
        div[data-testid="stHorizontalBlock"] > div {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        
        div[data-testid="stHorizontalBlock"] > div:hover {
            transform: translateY(-5px);
        }
        
        /* Buttons */
        .stButton button {
            width: 100%;
            border-radius: 5px;
            background-color: #1E88E5;
            color: white;
            font-weight: 500;
            padding: 0.5rem 1rem;
            margin: 0.5rem 0;
            transition: background-color 0.2s;
        }
        
        .stButton button:hover {
            background-color: #1565C0;
        }
        
        /* Form inputs */
        .stTextInput input {
            border-radius: 5px;
            border: 1px solid #E0E0E0;
            padding: 0.5rem;
        }
        
        .stTextArea textarea {
            border-radius: 5px;
            border: 1px solid #E0E0E0;
            padding: 0.5rem;
        }
        
        /* Success/Error messages */
        .success-message {
            background-color: #4CAF50;
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .error-message {
            background-color: #f44336;
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
