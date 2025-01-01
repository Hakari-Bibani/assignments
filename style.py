import streamlit as st

def app_style():
    """Apply custom styling to the Streamlit app"""
    
    # Custom CSS for the entire app
    st.markdown("""
        <style>
        /* Main content styling */
        .main {
            padding: 2rem;
        }
        
        /* Card styling for weeks and quizzes */
        .stButton button {
            width: 100%;
            height: 100px;
            margin: 10px 0;
            background-color: #f0f2f6;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            transition: all 0.3s;
        }
        
        .stButton button:hover {
            background-color: #e0e2e6;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Header styling */
        h1 {
            color: #1f1f1f;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
        }
        
        h2 {
            color: #2c3e50;
            font-size: 2rem;
            font-weight: 600;
            margin: 1.5rem 0;
        }
        
        h3 {
            color: #34495e;
            font-size: 1.5rem;
            font-weight: 500;
            margin: 1rem 0;
        }
        
        /* Form input styling */
        .stTextInput input {
            border-radius: 5px;
            border: 1px solid #e0e0e0;
            padding: 0.5rem;
        }
        
        .stTextArea textarea {
            border-radius: 5px;
            border: 1px solid #e0e0e0;
            padding: 0.5rem;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* Success/Error message styling */
        .stSuccess {
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .stError {
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        
        /* Code input area styling */
        .stCodeEditor {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* Custom card classes */
        .assignment-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        .quiz-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #45a049;
        }
        
        /* Table styling */
        .dataframe {
            border-collapse: collapse;
            margin: 1rem 0;
            width: 100%;
        }
        
        .dataframe th {
            background-color: #f8f9fa;
            padding: 0.75rem;
            text-align: left;
            border-bottom: 2px solid #dee2e6;
        }
        
        .dataframe td {
            padding: 0.75rem;
            border-bottom: 1px solid #dee2e6;
        }
        
        /* Progress bar styling */
        .stProgress > div > div {
            background-color: #4CAF50;
        }
        
        /* Custom container for assignment description */
        .assignment-description {
            background-color: #f8f9fa;
            padding: 1rem;
            border-left: 4px solid #4CAF50;
            margin: 1rem 0;
        }
        
        /* Metrics styling */
        .stMetric {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

def inject_custom_css():
    """Inject additional custom CSS for specific components"""
    st.markdown("""
        <style>
        /* Custom styles for specific components */
        div[data-testid="stToolbar"] {
            display: none;
        }
        
        div[data-testid="stDecoration"] {
            display: none;
        }
        
        section[data-testid="stSidebar"] > div {
            background-color: #f8f9fa;
            padding: 2rem 1rem;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def apply_theme():
    """Apply custom theme settings"""
    st.set_option('theme.primaryColor', '#4CAF50')
    st.set_option('theme.backgroundColor', '#ffffff')
    st.set_option('theme.secondaryBackgroundColor', '#f0f2f6')
    st.set_option('theme.textColor', '#1f1f1f')
    st.set_option('theme.font', 'sans-serif')

def init_styles():
    """Initialize all styling components"""
    app_style()
    inject_custom_css()
    apply_theme()

# Helper functions for custom components
def create_card(title, content, card_type="assignment"):
    """Create a custom card component"""
    card_class = "assignment-card" if card_type == "assignment" else "quiz-card"
    st.markdown(f"""
        <div class="{card_class}">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)

def create_info_box(message, type="info"):
    """Create a custom info box"""
    colors = {
        "info": "#17a2b8",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545"
    }
    st.markdown(f"""
        <div style="
            padding: 1rem;
            border-radius: 5px;
            background-color: {colors[type]}20;
            border-left: 4px solid {colors[type]};
            margin: 1rem 0;
        ">
            {message}
        </div>
    """, unsafe_allow_html=True)
