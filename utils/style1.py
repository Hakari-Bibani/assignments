import contextlib
import sys
from io import StringIO
import streamlit as st

@contextlib.contextmanager
def capture_output():
    """Capture standard output to display execution results."""
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out

def execute_code(code_string):
    """Execute code and capture its output."""
    with capture_output() as s:
        try:
            local_vars = {}  # Local namespace for the executed code
            exec(code_string, globals(), local_vars)
            output = s.getvalue()
            return output, None, local_vars
        except Exception as e:
            return None, str(e), None

def display_output(output, error):
    """Display execution results or errors in Streamlit."""
    if error:
        st.markdown(f"""
        <div style='color: red; font-family: monospace; padding: 10px; 
                    background-color: #f8f9fa; border-left: 3px solid red;'>
        {error}
        </div>
        """, unsafe_allow_html=True)
    elif output:
        st.markdown(f"""
        <div style='font-family: monospace; padding: 10px; 
                    background-color: #f8f9fa; border-left: 3px solid #2196F3;'>
        {output}
        </div>
        """, unsafe_allow_html=True)

