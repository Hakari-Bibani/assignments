import streamlit as st
import pandas as pd
from pathlib import Path
import importlib

def load_style():
    with open('style.py', 'r') as file:
        st.markdown(file.read(), unsafe_allow_html=True)

def create_card(title, description, link):
    with st.container():
        st.markdown(f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{description}</p>
            <a href="{link}" target="_self">Open</a>
        </div>
        """, unsafe_allow_html=True)

def main():
    st.title("Programming Assignments Portal")
    load_style()
    
    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Weekly Assignments")
        for week in range(1, 16):
            create_card(
                f"Week {week}",
                f"Assignment for Week {week}",
                f"Week_{week}"
            )
    
    with col2:
        st.header("Quizzes")
        for quiz in range(1, 11):
            create_card(
                f"Quiz {quiz}",
                f"Quiz {quiz}",
                f"Quiz_{quiz}"
            )
