import streamlit as st
from style import apply_custom_style, create_card, create_section_header

# Apply custom styling
apply_custom_style()

# Set page config
st.set_page_config(
    page_title="ImpactHub",
    page_icon="🎓",
    layout="wide"
)

# Animated title
st.markdown('<div class="sliding-title">ImpactHub</div>', unsafe_allow_html=True)

# Create two columns for Weeks and Quizzes
col1, col2 = st.columns(2)

with col1:
    create_section_header("Weekly Assignments")
    for week in range(1, 16):
        create_card(
            f"Week {week}",
            f"Assignment for Week {week}",
            f"week{week}"
        )

with col2:
    create_section_header("Quizzes")
    for quiz in range(1, 11):
        create_card(
            f"Quiz {quiz}",
            f"Take Quiz {quiz}",
            f"quiz{quiz}"
        )

# Add JavaScript for handling card clicks
st.markdown("""
    <script>
    function handleClick(key) {
        if (key.startsWith('week')) {
            window.location.href = f"/pages/{key}";
        } else if (key.startsWith('quiz')) {
            window.location.href = f"/pages/{key}";
        }
    }
    </script>
""", unsafe_allow_html=True)
