def apply_custom_style():
    st.markdown("""
        <style>
        /* Moving title animation */
        @keyframes moveTitle {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .moving-title {
            overflow: hidden;
            white-space: nowrap;
            margin-bottom: 2rem;
        }
        
        .moving-title h1 {
            display: inline-block;
            color: red;
            font-size: 3.5rem;
            animation: moveTitle 15s linear infinite;
        }
        
        /* Card styling */
        .card {
            padding: 1.5rem;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: #1f1f1f;
            margin-bottom: 0.5rem;
        }
        
        .card p {
            color: #666;
            margin: 0;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        
        /* Button styling */
        .stButton button {
            width: 100%;
            margin-bottom: 0.5rem;
            background-color: #ffffff;
            border: 1px solid #ddd;
            transition: background-color 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)
