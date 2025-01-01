import streamlit as st
import streamlit.components.v1 as components

# Custom CSS for styling
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        color: red;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# Main title
st.markdown('<p class="big-font">ImpactHub</p>', unsafe_allow_html=True)

# Display Weeks
st.header("Weeks")
for i in range(1, 16):
    if st.button(f"Week {i}", key=f"week{i}"):
        st.experimental_rerun()

# Display Quizzes
st.header("Quizzes")
for i in range(1, 11):
    if st.button(f"Quiz {i}", key=f"quiz{i}"):
        st.experimental_rerun()
