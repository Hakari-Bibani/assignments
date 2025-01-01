import streamlit as st

def apply_custom_style():
    """Apply custom styling to the Streamlit app"""
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes slide {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .sliding-title {
            color: red;
            font-size: 4rem;
            font-weight: bold;
            white-space: nowrap;
            overflow: hidden;
            animation: slide 8s linear infinite;
        }
        
        /* Card styling */
        .stcard {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .stcard:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Section headers */
        .section-header {
            color: #1E88E5;
            font-size: 2rem;
            font-weight: bold;
            margin: 30px 0 20px 0;
        }
        
        /* Code input area */
        .stTextInput>div>div>textarea {
            font-family: 'Courier New', Courier, monospace;
            background-color: #f8f9fa;
        }
        </style>
    """, unsafe_allow_html=True)

def create_card(title, description="", key=None):
    """Create a styled card with hover effects"""
    card_html = f"""
        <div class="stcard" onclick="handleClick('{key}')" style="cursor: pointer;">
            <h3 style="margin: 0; color: #2196F3;">{title}</h3>
            <p style="margin: 10px 0 0 0; color: #666;">{description}</p>
        </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

def create_section_header(title):
    """Create a styled section header"""
    return st.markdown(f'<h2 class="section-header">{title}</h2>', unsafe_allow_html=True)
