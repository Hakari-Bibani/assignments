import streamlit as st
from style import apply_custom_style
import time

# Apply custom styling
apply_custom_style()

# Title animation function
def animate_title():
    title_text = "ImpactHub"
    title_placeholder = st.empty()
    while True:
        title_placeholder.markdown(f'<h1 class="moving-title">{title_text}</h1>', unsafe_allow_html=True)
        time.sleep(0.1)

# Main layout
st.markdown("""
    <style>
    .moving-title {
        color: red;
        font-size: 4em;
        text-align: center;
        animation: moveTitle 2s infinite;
    }
    
    @keyframes moveTitle {
        0% { transform: translateX(0); }
        50% { transform: translateX(20px); }
        100% { transform: translateX(0); }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="moving-title">ImpactHub</h1>', unsafe_allow_html=True)

# Create two columns for Weeks and Quizzes
col1, col2 = st.columns(2)

# Weeks Section
with col1:
    st.markdown("<h2 style='text-align: center;'>Weekly Assignments</h2>", unsafe_allow_html=True)
    weeks = [f"Week {i}" for i in range(1, 16)]
    for week in weeks:
        if st.button(week, key=f"btn_{week}", use_container_width=True):
            # Import and run the corresponding week's script
            try:
                module_name = f"week{week.split()[-1]}"
                exec(f"import {module_name}")
                exec(f"{module_name}.main()")
            except Exception as e:
                st.error(f"Error loading {week}: {str(e)}")

# Quizzes Section
with col2:
    st.markdown("<h2 style='text-align: center;'>Quizzes</h2>", unsafe_allow_html=True)
    quizzes = [f"Quiz {i}" for i in range(1, 11)]
    for quiz in quizzes:
        if st.button(quiz, key=f"btn_{quiz}", use_container_width=True):
            # Import and run the corresponding quiz script
            try:
                module_name = f"quiz{quiz.split()[-1]}"
                exec(f"import {module_name}")
                exec(f"{module_name}.main()")
            except Exception as e:
                st.error(f"Error loading {quiz}: {str(e)}")

if __name__ == "__main__":
    animate_title()
