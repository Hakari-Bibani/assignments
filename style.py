import streamlit as st

def apply_custom_style():
    """Apply custom styling to the Streamlit app"""
    st.markdown("""
        <style>
        /* Main container */
        .main {
            padding: 2rem;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #f0f2f6;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            color: #31333F;
            margin: 5px 0;
            transition: all 0.3s ease;
            width: 100%;
            padding: 10px;
        }
        
        .stButton > button:hover {
            background-color: #0066cc;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        /* Headers */
        h1 {
            color: red;
            text-align: center;
            font-size: 3em;
            margin-bottom: 2rem;
        }
        
        h2 {
            color: #31333F;
            margin-bottom: 1rem;
        }
        
        /* Columns spacing */
        .column {
            padding: 1rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Card styling */
        .stButton > button {
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)
