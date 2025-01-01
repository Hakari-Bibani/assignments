def apply_styles():
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes moveText {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .moving-title {
            overflow: hidden;
            white-space: nowrap;
        }
        
        .moving-title h1 {
            display: inline-block;
            animation: moveText 15s linear infinite;
            color: red;
            font-size: 4em;
            font-weight: bold;
        }
        
        /* Card styling */
        .stCard {
            transition: transform 0.3s ease;
            cursor: pointer;
        }
        
        .stCard:hover {
            transform: scale(1.05);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        
        /* Button styling */
        .stButton>button {
            width: 100%;
            margin: 0.2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
