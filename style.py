import streamlit as st

def apply_custom_style():
    """Apply custom styling to the Streamlit app"""
    st.markdown(
        """
        <style>
        /* Main title styling */
        .animated-title {
            text-align: center;
            animation: float 3s ease-in-out infinite;
        }
        
        .animated-title h1 {
            color: #FF0000;
            font-size: 4rem;
            font-weight: bold;
            margin: 2rem 0;
        }
        
        /* Animation keyframes */
        @keyframes float {
            0% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
            100% {
                transform: translateY(0px);
            }
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            margin: 0.5rem 0;
            border-radius: 5px;
            background-color: #f0f2f6;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #FF0000;
            color: white;
        }
        
        /* Column styling */
        .css-1r6slb0 {
            padding: 1rem;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Header styling */
        h2 {
            color: #333333;
            border-bottom: 2px solid #FF0000;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
