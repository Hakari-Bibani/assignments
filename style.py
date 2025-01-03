import streamlit as st

def apply_style():
    # Custom CSS for the main page
    st.markdown(
        """
        <style>
        @keyframes moveTitle {
            0% { transform: translateX(0); }
            50% { transform: translateX(20px); }
            100% { transform: translateX(0); }
        }
        h1 {
            color: red;
            font-size: 3.5em;
            animation: moveTitle 2s infinite;
            text-align: center;
        }
        .stExpander {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
