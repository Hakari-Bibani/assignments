import streamlit as st

def apply_style():
    st.markdown("""
    <style>
    /* Title Animation */
    .animated-title {
        color: red;
        animation: moveText 2s infinite;
        text-align: center;
    }
    
    @keyframes moveText {
        0% { transform: translateX(-20px); }
        50% { transform: translateX(20px); }
        100% { transform: translateX(-20px); }
    }
    
    /* Flip Card Styles */
    .flip-card {
        background-color: transparent;
        width: 100%;
        height: 180px;
        perspective: 1000px;
        margin: 10px 0;
    }
    
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }
    
    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }
    
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
    }
    
    .flip-card-front {
        background-color: #2C3E50;
        color: white;
    }
    
    .flip-card-back {
        background-color: #34495E;
        color: white;
        transform: rotateY(180deg);
    }
    </style>
    """, unsafe_allow_html=True)
