import streamlit as st

st.title("Assignments and Quizzes")

pages = {
    "Week 1": "pages/week1.py",
    "Week 2": "pages/week2.py",
    # Add all weeks and quizzes here
}

choice = st.sidebar.selectbox("Select a page", list(pages.keys()))
exec(open(pages[choice]).read())
