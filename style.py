import streamlit as st

def apply_custom_styles():
    # Custom CSS
    st.markdown("""
        <style>
        /* Moving title animation */
        @keyframes moveTitle {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .moving-title {
            overflow: hidden;
            white-space: nowrap;
            margin-bottom: 2rem;
        }
        
        .moving-title h1 {
            display: inline-block;
            font-size: 3.5rem;
            animation: moveTitle 15s linear infinite;
            color: #2E86C1;
        }
        
        /* Flip card styles */
        .flip-card {
            background-color: transparent;
            width: 300px;
            height: 150px;
            perspective: 1000px;
            margin: 20px auto;
            cursor: pointer;
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
            background-color: #2E86C1;
            color: white;
        }

        .flip-card-back {
            background-color: #1B4F72;
            color: white;
            transform: rotateY(180deg);
        }

        /* Additional styles */
        h2 {
            color: #2E86C1;
            margin-bottom: 2rem;
        }

        .stButton button {
            width: 100%;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
