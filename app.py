import streamlit as st
import importlib
from style import apply_style

def load_page(page_name, page_number):
    """Load assignment or quiz page"""
    if page_name == 'assignment':
        module_name = f'as{page_number}'
    else:  # quiz
        module_name = f'quiz{page_number}'
    
    try:
        # Clear the main page content
        st.empty()
        
        # Import and display the selected module
        module = importlib.import_module(module_name)
        
        # Add a back button
        if st.button("← Back to Main Page"):
            st.session_state.current_page = 'main'
            st.experimental_rerun()
            
        # Display the module content
        if hasattr(module, 'main'):
            module.main()
    except ImportError:
        st.error(f"Unable to load {module_name}. Make sure the file exists.")

def create_flip_card(title, description, page_type, number):
    """Create a flip card with navigation"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class='flip-card' id='{page_type}_{number}'>
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
        
        with col2:
            if st.button(f"Open {title}", key=f"btn_{page_type}_{number}"):
                st.session_state.current_page = f"{page_type}_{number}"
                st.experimental_rerun()

def main_page():
    """Display the main page with flip cards"""
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

    with tab1:
        st.markdown("## Assignments")
        for i in range(1, 16):
            create_flip_card(
                f"Assignment {i}",
                f"Click to view and submit Assignment {i}",
                "assignment",
                i
            )

    with tab2:
        st.markdown("## Quizzes")
        for i in range(1, 11):
            create_flip_card(
                f"Quiz {i}",
                f"Click to take Quiz {i}",
                "quiz",
                i
            )

def main():
    """Main application logic"""
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'
    
    # Handle navigation
    if st.session_state.current_page == 'main':
        main_page()
    else:
        # Parse the current page to get type and number
        page_type, page_number = st.session_state.current_page.split('_')
        load_page(page_type, page_number)

if __name__ == "__main__":
    main()
