import streamlit as st

def custom_style():
    st.markdown("""
        <style>
        /* Main page styling */
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        /* Headers styling */
        h1 {
            color: #2c3e50;
            text-align: center;
            padding: 20px 0;
        }
        
        h2 {
            color: #34495e;
            padding: 15px 0;
        }
        
        /* Card styling */
        .css-1r6slb0 {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        
        /* Input fields styling */
        .stTextInput > div > div > input {
            border-radius: 5px;
        }
        
        /* General page styling */
        .main {
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        </style>
    """, unsafe_allow_html=True)
