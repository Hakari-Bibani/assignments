import streamlit as st
from style import apply_custom_style
import importlib
import os
import inspect

# Page configuration
st.set_page_config(
    page_title="ImpactHub",
    page_icon="🎓",
    layout="wide"
)

# Apply custom styling
st.markdown(apply_custom_style(), unsafe_allow_html=True)

# Session state initialization
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'
if 'current_module' not in st.session_state:
    st.session_state.current_module = None

def navigate_to_module(module_name):
    """Handle navigation to a specific module"""
    try:
        # First try to import the assignment module
        assignment_module = importlib.import_module(module_name)
        # Then try to import the corresponding grading module
        grade_module = importlib.import_module(f"grade{module_name.replace('week', '').replace('quiz', '')}")
        
        st.session_state.current_page = module_name
        st.session_state.current_module = {
            'assignment': assignment_module,
            'grading': grade_module
        }
    except ImportError as e:
        st.error(f"Could not load module: {str(e)}")

def create_card(title, module_name):
    """Create a card with navigation button"""
    with st.container():
        st.markdown(f'''
        <div class="card">
            <h3>{title}</h3>
        </div>
        ''', unsafe_allow_html=True)
        if st.button(f"Start", key=f"start_{module_name}"):
            navigate_to_module(module_name)

def show_main_page():
    """Display the main page with all cards"""
    # Main title with animation
    st.markdown('<h1 class="main-title">ImpactHub</h1>', unsafe_allow_html=True)

    # Create two columns for Weeks and Quizzes
    col1, col2 = st.columns(2)

    # Weeks section
    with col1:
        st.markdown('<h2 class="section-title">Weekly Assignments</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        for week in range(1, 16):
            create_card(f"Week {week}", f"week{week}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Quizzes section
    with col2:
        st.markdown('<h2 class="section-title">Quizzes</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        for quiz in range(1, 11):
            create_card(f"Quiz {quiz}", f"quiz{quiz}")
        st.markdown('</div>', unsafe_allow_html=True)

def show_module_page():
    """Display the current module page"""
    if st.button("← Back to Main Page"):
        st.session_state.current_page = 'main'
        st.rerun()

    module = st.session_state.current_module
    if module:
        # Display assignment content
        if hasattr(module['assignment'], 'main'):
            module['assignment'].main()
        
        # Display grading section
        st.markdown("---")
        st.header("Grading")
        if hasattr(module['grading'], 'grade'):
            result = module['grading'].grade()
            if result:
                # Save grade to CSV
                save_grade(st.session_state.current_page, result)

def save_grade(module_name, grade_result):
    """Save grading results to CSV"""
    import pandas as pd
    import datetime
    
    # Ensure the grades directory exists
    os.makedirs('grades', exist_ok=True)
    
    # Create or load the submission CSV
    csv_path = 'grades/data_submission.csv'
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['timestamp', 'module', 'grade'])
    
    # Add new submission
    new_row = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'module': module_name,
        'grade': grade_result
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Save to CSV
    df.to_csv(csv_path, index=False)
    st.success(f"Grade saved successfully: {grade_result}")

# Main app logic
if st.session_state.current_page == 'main':
    show_main_page()
else:
    show_module_page()

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; background-color: #f0f2f6;">
    <p>© 2025 ImpactHub. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
