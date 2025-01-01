import streamlit as st

def set_custom_style():
    custom_css = """
    <style>
    @keyframes move {
        0% { transform: translateX(0); }
        50% { transform: translateX(20px); }
        100% { transform: translateX(0); }
    }
    
    .title {
        font-size: 48px;
        color: red;
        text-align: center;
        animation: move 2s infinite;
        font-weight: bold;
        margin-bottom: 30px;
    }
    
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
        padding: 20px;
    }
    
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .tab-button {
        width: 100%;
        padding: 8px;
        background-color: #f0f0f0;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }
    
    .tab-button:hover {
        background-color: #e0e0e0;
    }
    
    .section-title {
        font-size: 24px;
        color: #333;
        margin: 20px 0;
        padding-left: 20px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
