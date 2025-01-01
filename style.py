import streamlit as st

def apply_style():
    """Apply custom styling to the Streamlit app"""
    st.markdown("""
        <style>
        /* Main container */
        .main {
            padding: 2rem;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            margin: 5px 0;
            background-color: #f0f2f6;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 10px;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #e0e0e0;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Headers */
        h3 {
            color: #1f1f1f;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f2f6;
            margin-bottom: 20px;
        }
        
        /* Columns layout */
        .row-widget.stHorizontal {
            gap: 2rem;
        }
        
        /* Card-like styling for buttons */
        .stButton > button {
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        
        /* Hover effect for cards */
        .stButton > button:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Animation for title */
        @keyframes glow {
            0% { text-shadow: 0 0 10px rgba(255,0,0,0.5); }
            50% { text-shadow: 0 0 20px rgba(255,0,0,0.7); }
            100% { text-shadow: 0 0 10px rgba(255,0,0,0.5); }
        }
        
        .title {
            animation: glow 2s ease-in-out infinite;
        }
        </style>
    """, unsafe_allow_html=True)
