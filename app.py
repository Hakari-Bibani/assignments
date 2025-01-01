import streamlit as st
import pandas as pd
from style import set_custom_style

def main():
    set_custom_style()
    
    # Set page config
    st.set_page_config(
        page_title="ImpactHub",
        page_icon="📚",
        layout="wide"
    )
    
    # Title with animation
    st.markdown('<h1 class="title">ImpactHub</h1>', unsafe_allow_html=True)
    
    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="section-title">Weekly Assignments</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        for week in range(1, 16):
            with st.container():
                st.markdown(f'''
                <div class="card">
                    <h3>Week {week}</h3>
                    <p>Assignment {week}</p>
                    <button class="tab-button" onclick="window.location.href='week{week}.py'">Start</button>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h2 class="section-title">Quizzes</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        for quiz in range(1, 11):
            with st.container():
                st.markdown(f'''
                <div class="card">
                    <h3>Quiz {quiz}</h3>
                    <p>Assessment {quiz}</p>
                    <button class="tab-button" onclick="window.location.href='quiz{quiz}.py'">Start</button>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
