import streamlit as st

def apply_style():
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Flip card container */
        .flip-card {
            background-color: transparent;
            width: 300px;
            height: 200px;
            perspective: 1000px;
            margin: 20px auto;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .flip-card:hover {
            transform: translateY(-10px);
        }
        
        /* Flip card inner container */
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
        
        /* Front and back styles */
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .flip-card-front {
            background: linear-gradient(145deg, #1E88E5, #1565C0);
            color: white;
        }
        
        .flip-card-back {
            background: linear-gradient(145deg, #1565C0, #0D47A1);
            color: white;
            transform: rotateY(180deg);
        }
        
        /* Text styling */
        .flip-card h3 {
            margin: 0;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .flip-card p {
            margin: 0;
            font-size: 1.2em;
        }
        
        /* Custom button styling */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            background-color: #1E88E5;
            color: white;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #1565C0;
            transform: scale(1.05);
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
