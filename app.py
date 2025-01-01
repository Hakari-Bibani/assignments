import streamlit as st

# Import custom styles
from style import apply_card_style, set_page_theme

# Set the page theme
set_page_theme()

# Main page layout
st.title("Course Management Platform")

# Display cards for Assignments and Quizzes
st.header("Assignments")
for week in range(1, 16):
    if st.button(f"Week {week}"):
        st.query_params(page=f"week{week}")

st.header("Quizzes")
for quiz in range(1, 11):
    if st.button(f"Quiz {quiz}"):
        st.query_params(page=f"quiz{quiz}")

# Handle navigation
query_params = st.query_params()
if "page" in query_params:
    page = query_params["page"][0]
    st.write(f"Navigating to {page}.py")
    # Here you would include logic to load the respective page content
