import streamlit as st
from style import apply_style  # Import custom styling

# Apply custom styling
apply_style()

# Main page layout
st.title("Online Assignments and Quizzes Manager")

# Flip cards for Assignments
st.header("Assignments")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Assignment 1"):
        st.switch_page("pages/as1.py")
with col2:
    if st.button("Assignment 2"):
        st.switch_page("pages/as2.py")
# Add more columns/buttons for assignments 3-15...

# Flip cards for Quizzes
st.header("Quizzes")
col4, col5, col6 = st.columns(3)
with col4:
    if st.button("Quiz 1"):
        st.switch_page("pages/quiz1.py")
with col5:
    if st.button("Quiz 2"):
        st.switch_page("pages/quiz2.py")
# Add more columns/buttons for quizzes 3-10...

# Footer
st.markdown("---")
st.markdown("© 2023 Your Organization Name")
