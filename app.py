import streamlit as st
import base64
from pathlib import Path

def load_local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def create_flip_card(title, description, link):
    card_html = f'''
    <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
                <h2>{title}</h2>
            </div>
            <div class="flip-card-back">
                <p>{description}</p>
                <div class="tab-navigation">
                    <a href="{link}" target="_self" class="tab-button">Go to {title}</a>
                </div>
            </div>
        </div>
    </div>
    '''
    return card_html

def main():
    st.set_page_config(page_title="ImpactHub", layout="wide")
    load_local_css("style.py")

    # Title with animation
    st.markdown('<h1 class="moving-title">ImpactHub</h1>', unsafe_allow_html=True)

    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2>Assignments</h2>", unsafe_allow_html=True)
        for i in range(1, 16):
            card_html = create_flip_card(
                f"Assignment {i}",
                f"Click to access Assignment {i}",
                f"/as{i}"
            )
            st.markdown(card_html, unsafe_allow_html=True)

    with col2:
        st.markdown("<h2>Quizzes</h2>", unsafe_allow_html=True)
        for i in range(1, 11):
            card_html = create_flip_card(
                f"Quiz {i}",
                f"Click to access Quiz {i}",
                f"/quiz{i}"
            )
            st.markdown(card_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
