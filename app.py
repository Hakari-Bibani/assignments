import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc
from style import set_styles
import pandas as pd

def main():
    st.set_page_config(
        page_title="ImpactHub",
        page_icon="📚",
        layout="wide"
    )
    
    set_styles()
    
    # Title with animation
    st.markdown('<h1 class="main-title">ImpactHub</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        menu_items = {
            "Weeks": [f"Week {i}" for i in range(1, 16)],
            "Quizzes": [f"Quiz {i}" for i in range(1, 11)]
        }
        
        selected = option_menu(
            "Menu",
            ["Weeks", "Quizzes"],
            icons=["book", "pencil-square"],
            default_index=0,
        )
        
        if selected == "Weeks":
            for week in menu_items["Weeks"]:
                if st.button(week):
                    st.switch_page(f"pages/week{week.split()[-1]}.py")
        else:
            for quiz in menu_items["Quizzes"]:
                if st.button(quiz):
                    st.switch_page(f"pages/quiz{quiz.split()[-1]}.py")
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="weeks-section">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Weeks</p>', unsafe_allow_html=True)
        
        for i in range(1, 16, 2):
            # Create card for weeks
            with st.container():
                st.markdown(f'''
                    <div class="card" onclick="window.location.href='pages/week{i}.py'">
                        <h3>Week {i}</h3>
                        <p>Click to view assignments and grades for Week {i}</p>
                    </div>
                ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="quizzes-section">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Quizzes</p>', unsafe_allow_html=True)
        
        for i in range(1, 11, 2):
            # Create card for quizzes
            with st.container():
                st.markdown(f'''
                    <div class="card" onclick="window.location.href='pages/quiz{i}.py'">
                        <h3>Quiz {i}</h3>
                        <p>Click to view Quiz {i} and grades</p>
                    </div>
                ''', unsafe_allow_html=True)

    # Load and display grades from CSV
    try:
        grades_df = pd.read_csv('grades/data_submission.csv')
        if st.checkbox("Show All Grades"):
            st.dataframe(grades_df)
    except Exception as e:
        st.error("Error loading grades data. Please ensure the CSV file exists and is properly formatted.")

if __name__ == "__main__":
    main()
