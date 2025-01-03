import streamlit as st
import pandas as pd
import sys
import io
import json
import os
import importlib.util

# Import grade1 from the grades directory
def import_grader():
    # Construct the path to grade1.py
    grade_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'grades', 'grade1.py')
    
    # Import the module dynamically
    spec = importlib.util.spec_from_file_location("grade1", grade_path)
    grade_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(grade_module)
    
    return grade_module.grade_assignment

# Get the grading function
grade_assignment = import_grader()

def main():
    st.title("Week 1 Assignment - Mapping Coordinates and Calculating Distances")
    
    # Rest of the code remains the same...
    [Previous code for main() function]

if __name__ == "__main__":
    main()
