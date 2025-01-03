def apply_style():
    """
    Applies custom styling to the Streamlit app.
    """
    st.markdown(
        """
        <style>
        /* Main title styling */
        h1 {
            color: #4F8BF9;
            text-align: center;
        }
        /* Header styling */
        h2 {
            color: #2E86C1;
        }
        /* Button styling */
        .stButton button {
            background-color: #4F8BF9;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #2E86C1;
        }
        /* Footer styling */
        .footer {
            text-align: center;
            font-size: 14px;
            color: #777;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
