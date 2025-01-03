import streamlit as st
import importlib
from style import apply_style

def load_assignment_module(assignment_number):
    try:
        module = importlib.import_module(f'as{assignment_number}')
        return module
    except ImportError:
        return None

def load_quiz_module(quiz_number):
    try:
        module = importlib.import_module(f'quiz{quiz_number}')
        return module
    except ImportError:
        return None

def create_flip_card(title, description, link_text, key):
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        # Create a card-like container with hover effect
        with col1:
            card = st.container()
            with card:
                st.markdown(f"""
                <div class='flip-card' id='{key}'>
                    <div class='flip-card-inner'>
                        <div class='flip-card-front'>
                            <h3>{title}</h3>
                        </div>
                        <div class='flip-card-back'>
                            <p>{description}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Navigation button
        with col2:
            if st.button(f"Go to {link_text}", key=f"btn_{key}"):
                module = None
                if 'Assignment' in title:
                    assignment_num = int(title.split()[-1])
                    module = load_assignment_module(assignment_num)
                else:
                    quiz_num = int(title.split()[-1])
                    module = load_quiz_module(quiz_num)
                
                if module and hasattr(module, 'main'):
                    st.session_state.current_page = module.__name__
                    module.main()

def main():
    # Apply custom styling
    apply_style()
    
    # Title with animation
    st.markdown("""
        <div class="moving-title">
            <h1>ImpactHub</h1>
        </div>
    """, unsafe_allow_html=True)

    # Tabs for Assignments and Quizzes
    tab1, tab2 = st.tabs(["Assignments", "Quizzes"])

    # Assignments Section
    with tab1:
        st.markdown("## Assignments")
        for i in range(1, 16):
            create_flip_card(
                f"Assignment {i}",
                f"Click to view details for Assignment {i}",
                f"Assignment {i}",
                f"assignment_{i}"
            )

    # Quizzes Section
    with tab2:
        st.markdown("## Quizzes")
        for i in range(1, 11):
            create_flip_card(
                f"Quiz {i}",
                f"Click to view details for Quiz {i}",
                f"Quiz {i}",
                f"quiz_{i}"
            )

if __name__ == "__main__":
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'
    
    if st.session_state.current_page == 'main':
        main()
    else:
        module = importlib.import_module(st.session_state.current_page)
        module.main()
