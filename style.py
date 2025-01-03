import streamlit as st
import base64

def apply_style():
    st.markdown("""
        <style>
        @keyframes move {
            0% { transform: translateX(0); }
            50% { transform: translateX(20px); }
            100% { transform: translateX(0); }
        }
        
        .main-title {
            font-size: 4rem;
            color: red;
            text-align: center;
            animation: move 2s infinite;
        }
        
        .stExpander {
            background-color: #f0f2f6;
            border-radius: 10px;
            margin: 10px 0;
            padding: 10px;
            transition: transform 0.3s;
        }
        
        .stExpander:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }
        
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
        
        <div class="main-title">ImpactHub</div>
    """, unsafe_allow_html=True)
