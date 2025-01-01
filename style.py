def apply_styles():
    # Custom CSS with animation
    st.markdown("""
        <style>
        @keyframes moveText {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .moving-title {
            overflow: hidden;
            white-space: nowrap;
        }
        
        .moving-title h1 {
            color: red;
            font-size: 3em;
            display: inline-block;
            animation: moveText 10s linear infinite;
        }
        
        .stButton button {
            width: 100%;
            margin: 5px 0;
        }
        
        /* Card styling */
        .card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            transition: transform 0.3s;
        }
        
        .card:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
