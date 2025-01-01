import streamlit as st

def set_page_style():
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes colorChange {
            0% { color: #FF0000; }
            50% { color: #FF4444; }
            100% { color: #FF0000; }
        }
        
        .main-title {
            font-size: 3.5em;
            font-weight: bold;
            text-align: center;
            animation: colorChange 2s infinite;
            margin-bottom: 2em;
        }
        
        /* Card styling */
        .stCard {
            border-radius: 10px;
            padding: 1em;
            margin: 1em 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* List styling */
        .list-container {
            margin: 2em 0;
            padding: 1em;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .list-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 1em;
            color: #2c3e50;
        }
        
        /* Tab styling */
        .stTabs {
            margin-top: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

def create_card(title, description):
    return f"""
        <div class="stCard">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    """
