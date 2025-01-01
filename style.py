import streamlit as st

def apply_styles():
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes colorChange {
            0% { color: #ff0000; transform: scale(1); }
            50% { color: #ff4444; transform: scale(1.1); }
            100% { color: #ff0000; transform: scale(1); }
        }
        
        .animated-title {
            font-size: 4rem !important;
            text-align: center;
            font-weight: bold;
            animation: colorChange 2s infinite;
        }
        
        /* Card styling */
        .stExpander {
            background-color: #f0f2f6;
            border-radius: 10px;
            margin: 10px 0;
            padding: 10px;
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        
        .stButton button:hover {
            background-color: #45a049;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            padding: 20px;
        }
        
        /* Custom layout for columns */
        .row-widget.stRadio > div {
            flex-direction: row;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)
