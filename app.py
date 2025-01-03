import streamlit as st
import streamlit.components.v1 as components
from style import apply_style

def create_flip_card(title, description):
    return f"""
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
    """

def main():
    apply_style()
    
    # Title with animation
    st.markdown("""
        <h1 class="animated-title">ImpactHub</h1>
    """, unsafe_allow_html=True)
    
    # Assignments Section
    st.header("Assignments")
    cols = st.columns(3)
    for i in range(15):
        with cols[i % 3]:
            components.html(
                create_flip_card(f"Assignment {i+1}", 
                               f"Click to view Assignment {i+1}"),
                height=200
            )
    
    # Quizzes Section
    st.header("Quizzes")
    cols = st.columns(3)
    for i in range(10):
        with cols[i % 3]:
            components.html(
                create_flip_card(f"Quiz {i+1}", 
                               f"Click to view Quiz {i+1}"),
                height=200
            )

if __name__ == "__main__":
    main()
