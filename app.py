import streamlit as st
import style
from pathlib import Path

# Configure page settings
st.set_page_config(
    page_title="ImpactHub",
    page_icon="🎓",
    layout="wide"
)

# Apply custom styles
style.apply_custom_styles()

# Create title with animation effect
st.markdown(
    """
    <div class="marquee">
        <h1>ImpactHub</h1>
    </div>
    """,
    unsafe_allow_html=True
)

def create_card(title, description, link):
    """Create a clickable card with custom styling."""
    card_html = f"""
    <div class="card" onclick="window.location.href='{link}'">
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

def main():
    # Create container for cards
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    
    # Assignments Section
    st.markdown("<h2>Assignments</h2>", unsafe_allow_html=True)
    cols = st.columns(5)  # 5 cards per row
    
    for week in range(1, 16):
        with cols[(week-1) % 5]:
            create_card(
                f"Week {week}",
                f"Assignment for Week {week}",
                f"week{week}"
            )
    
    # Quizzes Section
    st.markdown("<h2>Quizzes</h2>", unsafe_allow_html=True)
    cols = st.columns(5)  # 5 cards per row
    
    for quiz in range(1, 11):
        with cols[(quiz-1) % 5]:
            create_card(
                f"Quiz {quiz}",
                f"Quiz {quiz} Assessment",
                f"quiz{quiz}"
            )

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
