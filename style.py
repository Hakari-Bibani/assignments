import streamlit as st

def set_page_style():
    # Custom CSS styles
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes colorChange {
            0% { color: #ff0000; }
            50% { color: #ff4444; }
            100% { color: #ff0000; }
        }
        
        .main-title {
            font-size: 3.5rem;
            font-weight: bold;
            text-align: center;
            animation: colorChange 2s infinite;
            margin-bottom: 2rem;
        }
        
        /* Card styles */
        .stcard {
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            background: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .stcard:hover {
            transform: translateY(-5px);
        }
        
        /* Section headers */
        .section-header {
            font-size: 2rem;
            font-weight: bold;
            color: #2c3e50;
            margin: 2rem 0 1rem 0;
        }
        
        /* Grid layout */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            padding: 1rem;
        }
        
        /* Custom button styles */
        .custom-button {
            background-color: #4CAF50;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
            display: block;
            margin: 0.5rem 0;
        }
        
        .custom-button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

def create_card(title, description, link):
    return f"""
        <a href="{link}" style="text-decoration: none;">
            <div class="stcard">
                <h3 style="color: #2c3e50;">{title}</h3>
                <p style="color: #7f8c8d;">{description}</p>
                <div class="custom-button">View Details</div>
            </div>
        </a>
    """
