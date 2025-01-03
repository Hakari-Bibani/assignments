import streamlit as st
import os
import style
from PIL import Image

def load_assignments():
    assignments = []
    for i in range(1, 16):
        assignments.append({
            'title': f'Assignment {i}',
            'description': f'Assignment {i} description',
            'link': f'Assignment_{i}'
        })
    return assignments

def load_quizzes():
    quizzes = []
    for i in range(1, 11):
        quizzes.append({
            'title': f'Quiz {i}',
            'description': f'Quiz {i} description',
            'link': f'Quiz_{i}'
        })
    return quizzes

def create_flip_card(title, description, link):
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'''
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <h3>{title}</h3>
                        </div>
                        <div class="flip-card-back">
                            <p>{description}</p>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            if st.button(f'Go to {title}', key=link):
                st.switch_page(f"pages/{link.lower()}.py")

def main():
    st.set_page_config(page_title="ImpactHub", layout="wide")
    style.apply_styles()
    
    # Title with animation
    st.markdown(style.get_animated_title(), unsafe_allow_html=True)
    
    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Assignments")
        assignments = load_assignments()
        for assignment in assignments:
            create_flip_card(
                assignment['title'],
                assignment['description'],
                assignment['link']
            )
    
    with col2:
        st.header("Quizzes")
        quizzes = load_quizzes()
        for quiz in quizzes:
            create_flip_card(
                quiz['title'],
                quiz['description'],
                quiz['link']
            )

if __name__ == "__main__":
    main()
