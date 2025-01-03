import streamlit as st
from streamlit_marquee import streamlit_marquee

def apply_style():
    # Custom CSS
    st.markdown("""
        <style>
        .title {
            font-size: 4em;
            color: red;
            text-align: center;
            animation: moveText 10s linear infinite;
        }
        
        @keyframes moveText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        .stExpander {
            background-color: #f0f2f6;
            border-radius: 10px;
            margin: 10px 0;
            transition: transform 0.3s;
        }
        
        .stExpander:hover {
            transform: scale(1.02);
        }
        
        .card {
            perspective: 1000px;
            transition: transform 0.8s;
            transform-style: preserve-3d;
        }
        
        .card:hover {
            transform: rotateY(180deg);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Animated title
    streamlit_marquee(
        text="ImpactHub",
        font_size="4em",
        text_color="red",
        background_color="transparent",
        speed=50
    )
