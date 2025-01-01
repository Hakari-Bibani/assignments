import streamlit as st
import pandas as pd
from style import set_page_style, create_card

# Set page configuration
st.set_page_config(
    page_title="ImpactHub",
    page_icon="📚",
    layout="wide"
)

# Apply custom styling
set_page_style()

# Display animated title
st.markdown('<h1 class="main-title">ImpactHub</h1>', unsafe_allow_html=True)

# Create two columns for Weeks and Quizzes
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2 class="section-header">Weekly Assignments</h2>', unsafe_allow_html=True)
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    
    # Generate cards for weeks
    for week in range(1, 16):
        card_html = create_card(
            f"Week {week}",
            f"Assignment and activities for Week {week}",
            f"/week{week}"
        )
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h2 class="section-header">Quizzes</h2>', unsafe_allow_html=True)
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    
    # Generate cards for quizzes
    for quiz in range(1, 11):
        card_html = create_card(
            f"Quiz {quiz}",
            f"Assessment quiz for Module {quiz}",
            f"/quiz{quiz}"
        )
        st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with grade information
st.markdown("---")
st.markdown("### Grade Information")

try:
    # Read the grades data
    grades_df = pd.read_csv('grades/data_submission.csv')
    
    # Display basic statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(grades_df))
    with col2:
        st.metric("Average Grade", f"{grades_df['Total'].mean():.2f}")
    with col3:
        st.metric("Submissions Today", len(grades_df[grades_df['Total'].notna()]))
        
except FileNotFoundError:
    st.warning("No grade data available yet. Start submitting assignments to see statistics.")
