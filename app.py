import streamlit as st
from streamlit.components.v1 import html

# Title with animation
st.markdown("<h1 style='color: red; animation: marquee 10s linear infinite;'>ImpactHub</h1>", unsafe_allow_html=True)

# CSS for animation
st.markdown("""
<style>
@keyframes marquee {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
h1 {
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# Display cards for Weeks and Quizzes
st.sidebar.title("Navigation")
weeks = [f"Week {i}" for i in range(1, 16)]
quizzes = [f"Quiz {i}" for i in range(1, 11)]

for week in weeks:
    if st.sidebar.button(week):
        st.experimental_rerun()

for quiz in quizzes:
    if st.sidebar.button(quiz):
        st.experimental_rerun()
