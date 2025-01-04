import streamlit as st
def apply_styles():
    st.markdown("""
        <style>
        /* Main title animation */
        .animate-title {
            animation: float 3s ease-in-out infinite;
        }
        .animate-title h1 {
            color: red;
            font-size: 4rem;
            text-align: center;
            font-weight: bold;
        }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
            100% { transform: translateY(0px); }
        }
        
        /* Flip card styles */
        .flip-card {
            background-color: transparent;
            width: 300px;
            height: 200px;
            perspective: 1000px;
            margin: 20px 0;
        }
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
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
            border-radius: 15px;
            padding: 20px;
        }
        .flip-card-front {
            background-color: #2c3e50;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .flip-card-back {
            background-color: #3498db;
            color: white;
            transform: rotateY(180deg);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .flip-card-back a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border: 2px solid white;
            border-radius: 5px;
            margin-top: 10px;
        }
        .flip-card-back a:hover {
            background-color: white;
            color: #3498db;
        }
        </style>
    """, unsafe_allow_html=True)
