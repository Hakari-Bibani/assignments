import streamlit as st
from streamlit_card import card
import style

def main():
    # Apply custom styles
    style.apply_custom_styles()
    
    # Title with animation
    st.markdown(
        """
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)

    # Weeks Section
    with col1:
        st.markdown("### Weeks")
        for week in range(1, 16):
            card_clicked = card(
                title=f"Week {week}",
                text="Click to view assignments",
                image=None,
                styles={
                    "card": {
                        "width": "100%",
                        "height": "100px",
                        "border-radius": "10px",
                        "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                        "margin-bottom": "10px",
                        "background-color": "#f0f2f6",
                        "cursor": "pointer"
                    }
                }
            )
            if card_clicked:
                st.switch_page(f"pages/week{week}.py")

    # Quizzes Section
    with col2:
        st.markdown("### Quizzes")
        for quiz in range(1, 11):
            card_clicked = card(
                title=f"Quiz {quiz}",
                text="Click to start quiz",
                image=None,
                styles={
                    "card": {
                        "width": "100%",
                        "height": "100px",
                        "border-radius": "10px",
                        "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                        "margin-bottom": "10px",
                        "background-color": "#e6f3ff",
                        "cursor": "pointer"
                    }
                }
            )
            if card_clicked:
                st.switch_page(f"pages/quiz{quiz}.py")

if __name__ == "__main__":
    main()
