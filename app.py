import streamlit as st
from streamlit_card import card
import webbrowser
from style import apply_style

def main():
    apply_style()
    
    st.title("ImpactHub")
    
    # Create two columns for Assignments and Quizzes
    col1, col2 = st.columns(2)
    
    # Assignments section
    with col1:
        st.header("Assignments")
        for i in range(1, 16):
            with st.expander(f"Assignment {i}"):
                card(
                    title=f"Assignment {i}",
                    text=f"Click to go to Assignment {i}",
                    image="",
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "200px",
                            "border-radius": "10px",
                            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                        }
                    }
                )
                if st.button(f"Go to Assignment {i}", key=f"as{i}"):
                    webbrowser.open(f"as{i}.py")

    # Quizzes section
    with col2:
        st.header("Quizzes")
        for i in range(1, 11):
            with st.expander(f"Quiz {i}"):
                card(
                    title=f"Quiz {i}",
                    text=f"Click to go to Quiz {i}",
                    image="",
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "200px",
                            "border-radius": "10px",
                            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                        }
                    }
                )
                if st.button(f"Go to Quiz {i}", key=f"quiz{i}"):
                    webbrowser.open(f"quiz{i}.py")

if __name__ == "__main__":
    main()
