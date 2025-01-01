import streamlit as st

# Configure page settings
st.set_page_config(page_title="ImpactHub", layout="wide")

# Custom CSS for moving title
st.markdown("""
    <style>
    @keyframes moveText {
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
        animation: moveText 15s linear infinite;
        color: red;
        font-size: 4rem;
        font-weight: bold;
    }
    
    .stButton > button {
        width: 100%;
        margin: 0.5rem 0;
        background-color: #f0f2f6;
        border: 1px solid #e0e3e9;
        border-radius: 5px;
        padding: 0.5rem;
    }
    
    h2 {
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Moving title
st.markdown("""
    <div class="moving-title">
        <h1>ImpactHub</h1>
    </div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2)

# Weeks Section
with col1:
    st.markdown("## Weeks")
    for week_num in range(1, 16):
        if st.button(f"Week {week_num}", key=f"week_{week_num}"):
            st.write(f"Loading Week {week_num} content...")

# Quizzes Section
with col2:
    st.markdown("## Quizzes")
    for quiz_num in range(1, 11):
        if st.button(f"Quiz {quiz_num}", key=f"quiz_{quiz_num}"):
            st.write(f"Loading Quiz {quiz_num} content...")

if __name__ == "__main__":
    pass
