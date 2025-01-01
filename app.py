import streamlit as st
import pandas as pd
from pathlib import Path
import importlib
import style

def load_css():
    with open("style.py") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Apply custom styles
    load_css()
    
    # Animated title
    st.markdown("""
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
    """, unsafe_allow_html=True)

    # Create grid layout for flip cards
    col1, col2, col3 = st.columns(3)
    
    # Weeks flip cards (1-15)
    weeks = list(range(1, 16))
    quizzes = list(range(1, 11))
    
    # Create flip cards for weeks
    for i, week in enumerate(weeks):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
                <div class="flip-card" onclick="window.location.href='week{week}'">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <h2>Week {week}</h2>
                        </div>
                        <div class="flip-card-back">
                            <p>Click to view Week {week} assignments</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create flip cards for quizzes
    for i, quiz in enumerate(quizzes):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
                <div class="flip-card" onclick="window.location.href='quiz{quiz}'">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <h2>Quiz {quiz}</h2>
                        </div>
                        <div class="flip-card-back">
                            <p>Click to view Quiz {quiz}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
