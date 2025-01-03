import streamlit as st
from style import apply_style  # Import custom styling

# Apply custom styling
apply_style()

# Main page title
st.title("ImpactHub")

# Display assignments and quizzes in flip cards
st.header("Assignments")
assignment_cols = st.columns(3)  # Display 3 assignments per row
for i in range(1, 16):
    with assignment_cols[(i - 1) % 3]:
        with st.expander(f"Assignment {i}"):
            st.write(f"Description for Assignment {i}")
            if st.button(f"Go to Assignment {i}", key=f"as{i}"):
                st.switch_page(f"pages/as{i}.py")  # Navigate to the assignment page

st.header("Quizzes")
quiz_cols = st.columns(3)  # Display 3 quizzes per row
for i in range(1, 11):
    with quiz_cols[(i - 1) % 3]:
        with st.expander(f"Quiz {i}"):
            st.write(f"Description for Quiz {i}")
            if st.button(f"Go to Quiz {i}", key=f"quiz{i}"):
                st.switch_page(f"pages/quiz{i}.py")  # Navigate to the quiz page
