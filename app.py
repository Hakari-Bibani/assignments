# app.py
import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from style import apply_style

# Configure page settings
st.set_page_config(
    page_title="ImpactHub",
    page_icon="📚",
    layout="wide"
)

# Apply custom styling
apply_style()

def create_pages_directory():
    # Create pages directory if it doesn't exist
    pages_dir = Path(current_dir) / "pages"
    pages_dir.mkdir(exist_ok=True)
    
    # Create symbolic links for week files
    for week in range(1, 16):
        week_file = pages_dir / f"{week}_Week_{week}.py"
        if not week_file.exists():
            original_file = Path(current_dir) / f"week{week}.py"
            if original_file.exists():
                week_file.write_text(f'''
import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import the week module
import week{week}

# Run the week's content
week{week}.run()
''')
    
    # Create symbolic links for quiz files
    for quiz in range(1, 11):
        quiz_file = pages_dir / f"{quiz+15}_Quiz_{quiz}.py"
        if not quiz_file.exists():
            original_file = Path(current_dir) / f"quiz{quiz}.py"
            if original_file.exists():
                quiz_file.write_text(f'''
import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import the quiz module
import quiz{quiz}

# Run the quiz content
quiz{quiz}.run()
''')

def main():
    # Create pages for navigation
    create_pages_directory()
    
    # Display animated title
    st.markdown("""
        <div class="animate-title">
            <h1>ImpactHub</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for weeks and quizzes
    col1, col2 = st.columns(2)
    
    # Weeks column
    with col1:
        st.markdown("### 📝 Weekly Assignments")
        for week in range(1, 16):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3>Week {week}</h3>
                    <p>Assignment {week}</p>
                </div>
                """, unsafe_allow_html=True)
                week_path = f"Week_{week}"
                st.link_button(f"Start Week {week}", week_path)
    
    # Quizzes column
    with col2:
        st.markdown("### 📊 Quizzes")
        for quiz in range(1, 11):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3>Quiz {quiz}</h3>
                    <p>Assessment {quiz}</p>
                </div>
                """, unsafe_allow_html=True)
                quiz_path = f"Quiz_{quiz}"
                st.link_button(f"Start Quiz {quiz}", quiz_path)

if __name__ == "__main__":
    main()
