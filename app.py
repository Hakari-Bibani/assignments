# app.py
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

# style.py
styles = """
/* Moving title animation */
@keyframes moveTitle {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.moving-title {
    overflow: hidden;
    white-space: nowrap;
    margin-bottom: 2rem;
}

.moving-title h1 {
    display: inline-block;
    animation: moveTitle 15s linear infinite;
    font-size: 3.5rem;
    color: #2E86C1;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

/* Flip card styles */
.flip-card {
    background-color: transparent;
    width: 100%;
    height: 200px;
    perspective: 1000px;
    margin-bottom: 1rem;
    cursor: pointer;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.6s;
    transform-style: preserve-3d;
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

.flip-card-front {
    background: linear-gradient(45deg, #2E86C1, #3498DB);
    color: white;
}

.flip-card-back {
    background: linear-gradient(45deg, #2ECC71, #27AE60);
    color: white;
    transform: rotateY(180deg);
}

.flip-card h2 {
    margin: 0;
    font-size: 1.5rem;
}

.flip-card p {
    margin: 0;
    font-size: 1rem;
}
"""

# requirements.txt
streamlit==1.31.0
pandas==2.1.4
pathlib==1.0.1
importlib-metadata==7.0.1
