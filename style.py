import streamlit as st

def apply_style():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        /* Moving red title */
        @keyframes moveTitle {
            0% { transform: translateX(0); }
            50% { transform: translateX(20px); }
            100% { transform: translateX(0); }
        }
        h1 {
            color: red;
            font-size: 3.5em;
            animation: moveTitle 2s infinite;
            text-align: center;
        }

        /* Flip card styling */
        .stExpander {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stExpander:hover {
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
