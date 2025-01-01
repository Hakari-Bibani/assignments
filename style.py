import streamlit as st

def set_styles():
    st.markdown("""
        <style>
        .main-title {
            font-size: 50px !important;
            color: red !important;
            text-align: center !important;
            animation: moveText 5s infinite linear;
        }
        
        @keyframes moveText {
            0% { transform: translateX(-20%); }
            50% { transform: translateX(20%); }
            100% { transform: translateX(-20%); }
        }
        
        .stButton>button {
            width: 100%;
            margin: 5px 0;
        }
        
        .card {
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            background-color: #f0f2f6;
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: scale(1.02);
            cursor: pointer;
        }
        
        .weeks-section, .quizzes-section {
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            background-color: #ffffff;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #1f75fe;
        }
        </style>
    """, unsafe_allow_html=True)
