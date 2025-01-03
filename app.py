import streamlit as st
import streamlit_card as sc
from style import apply_style
import importlib
import os

# Configure Streamlit page
st.set_page_config(
    page_title="ImpactHub",
    page_icon="📚",
    layout="wide"
)

# Apply custom styling
apply_style()

def load_module(module_name):
    """Dynamically import and run assignment/quiz modules"""
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, 'main'):
            module.main()
        else:
            st.error(f"No main function found in {module_name}")
    except ImportError as e:
        st.error(f"Could not load module {module_name}: {str(e)}")

def create_flip_card(title, description, key):
    """Create a flip card with hover effect"""
    card = sc.card(
        title=title,
        text=description,
        image="",
        key=key,
        styles={
            "card": {
                "width": "300px",
                "height": "200px",
                "border-radius": "10px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "transition": "transform 0.3s ease",
                ":hover": {
                    "transform": "scale(1.05)"
                }
            }
        }
    )
    return card

def main():
    # Animated title using custom CSS
    st.markdown("""
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Section:", ["Assignments", "Quizzes"])

    if page == "Assignments":
        st.header("Weekly Assignments")
        cols = st.columns(3)
        for week in range(1, 16):
            with cols[(week-1) % 3]:
                if create_flip_card(
                    f"Week {week}",
                    f"Click to view assignment for Week {week}",
                    f"week_{week}"
                ):
                    load_module(f"week{week}")

    else:  # Quizzes section
        st.header("Course Quizzes")
        cols = st.columns(3)
        for quiz in range(1, 11):
            with cols[(quiz-1) % 3]:
                if create_flip_card(
                    f"Quiz {quiz}",
                    f"Click to view Quiz {quiz}",
                    f"quiz_{quiz}"
                ):
                    load_module(f"quiz{quiz}")

if __name__ == "__main__":
    main()
