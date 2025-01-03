import streamlit as st
import base64

def apply_styles():
    """Apply custom styles to the Streamlit app"""
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes slideIn {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(0); }
        }
        
        .title-animation {
            color: #FF0000;
            font-size: 3.5em;
            font-weight: bold;
            animation: slideIn 2s ease-in-out infinite alternate;
            margin-bottom: 2em;
            text-align: center;
        }
        
        /* Flip card styles */
        .flip-card {
            background-color: transparent;
            width: 100%;
            height: 200px;
            perspective: 1000px;
            margin-bottom: 20px;
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
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .flip-card-front {
            background-color: #f8f9fa;
            color: #1e1e1e;
            padding: 20px;
        }
        
        .flip-card-back {
            background-color: #4CAF50;
            color: white;
            transform: rotateY(180deg);
            padding: 20px;
        }
        
        /* Custom container styles */
        .stContainer {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Custom button styles */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Custom title with animation
    st.markdown(
        '<h1 class="title-animation">ImpactHub</h1>',
        unsafe_allow_html=True
    )

def get_base64_encoded_image(image_path):
    """Get base64 encoded image"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def set_background_image(image_path):
    """Set background image"""
    encoded_image = get_base64_encoded_image(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
