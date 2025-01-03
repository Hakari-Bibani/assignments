import streamlit as st

def apply_style():
    st.markdown(
        """
        <style>
        /* Animated title */
        .animated-title {
            text-align: center;
            animation: colorChange 3s infinite;
        }
        
        .animated-title h1 {
            font-size: 4em;
            font-weight: bold;
            color: red;
        }
        
        @keyframes colorChange {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        /* Flip card styles */
        .flip-card {
            background-color: transparent;
            width: 200px;
            height: 100px;
            perspective: 1000px;
            margin: 10px;
        }
        
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            cursor: pointer;
        }
        
        .flip-card:hover .flip-card-inner {
            transform: rotateY(180deg);
        }
        
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .flip-card-front {
            background-color: #f8f9fa;
            color: #1f1f1f;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .flip-card-back {
            background-color: #4CAF50;
            color: white;
            transform: rotateY(180deg);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
