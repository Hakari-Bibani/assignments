import streamlit as st
import importlib
from style import apply_style

def load_assignment(number):
    try:
        module = importlib.import_module(f"as{number}")
        return module.run()
    except ImportError:
        st.error(f"Assignment {number} module not found")

def load_quiz(number):
    try:
        module = importlib.import_module(f"quiz{number}")
        return module.run()
    except ImportError:
        st.error(f"Quiz {number} module not found")

def main():
    apply_style()
    
    st.title("ImpactHub")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Assignments")
        for i in range(1, 16):
            with st.expander(f"Assignment {i}"):
                if st.button(f"Open Assignment {i}", key=f"as_{i}"):
                    load_assignment(i)
                
    with col2:
        st.header("Quizzes")
        for i in range(1, 11):
            with st.expander(f"Quiz {i}"):
                if st.button(f"Open Quiz {i}", key=f"quiz_{i}"):
                    load_quiz(i)

if __name__ == "__main__":
    main()
