import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
    
    # Custom CSS for the entire application
    st.markdown("""
        <style>
        /* Main title animation */
        @keyframes marquee {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        .marquee {
            width: 100%;
            overflow: hidden;
            white-space: nowrap;
            margin-bottom: 2rem;
        }
        
        .marquee h1 {
            display: inline-block;
            animation: marquee 15s linear infinite;
            color: #ff4b4b;
            font-size: 3rem;
            font-weight: bold;
        }
        
        /* Grid container for cards */
        .grid-container {
            display: grid;
            gap: 1rem;
            padding: 1rem;
        }
        
        /* Card styling */
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            margin-bottom: 1rem;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }
        
        .card h3 {
            color: #1f1f1f;
            margin-bottom: 0.5rem;
            font-size: 1.2rem;
        }
        
        .card p {
            color: #666;
            font-size: 0.9rem;
            margin: 0;
        }
        
        /* Section headers */
        h2 {
            color: #333;
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .card {
                padding: 1rem;
            }
            
            .marquee h1 {
                font-size: 2rem;
            }
            
            h2 {
                font-size: 1.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
