import streamlit as st
import folium
from geopy.distance import geodesic
import pandas as pd
from streamlit_folium import st_folium
from utils.style1 import execute_code, display_output
from github import Github
import base64
from datetime import datetime

# Constants for coordinates
COORDINATES = [
    (36.325735, 43.928414),  # Point 1
    (36.393432, 44.586781),  # Point 2
    (36.660477, 43.840174)   # Point 3
]

# Initialize GitHub settings
def init_github():
    try:
        return {
            'pat': st.secrets.github.pat,
            'repo': st.secrets.github.repo
        }
    except Exception as e:
        st.error("GitHub credentials not properly configured. Please check your Streamlit secrets configuration.")
        return None

def update_github_csv(submission_data):
    """
    Update the CSV file in GitHub repository
    """
    github_settings = init_github()
    if not github_settings:
        return False, "GitHub settings not properly configured"
    
    try:
        # Initialize GitHub with PAT
        g = Github(github_settings['pat'])
        repo = g.get_repo(github_settings['repo'])
        
        file_path = 'grades/data_submission.csv'
        try:
            # Try to get existing file
            contents = repo.get_contents(file_path)
            existing_data = base64.b64decode(contents.content).decode('utf-8')
            
            # Load existing data into DataFrame
            df = pd.read_csv(pd.StringIO(existing_data))
            
            # Update or add new submission
            if submission_data['Full name'] in df['Full name'].values:
                # Update existing student's data
                df.loc[df['Full name'] == submission_data['Full name'], 
                      ['email', 'student ID', 'assignment1']] = [
                          submission_data['email'],
                          submission_data['student ID'],
                          submission_data['assignment1']
                      ]
            else:
                # Add new student data
                new_row = pd.DataFrame([submission_data])
                df = pd.concat([df, new_row], ignore_index=True)
            
            # Recalculate total
            assignment_cols = [col for col in df.columns if col.startswith(('assignment', 'quiz'))]
            df['total'] = df[assignment_cols].sum(axis=1)
            
            # Convert updated DataFrame to CSV string
            updated_csv = df.to_csv(index=False)
            
            # Create commit message
            commit_message = f"Update submission data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Update file in repository
            repo.update_file(
                file_path,
                commit_message,
                updated_csv,
                contents.sha
            )
            return True, "Submission successfully saved"
            
        except Exception as e:
            return False, f"Error updating submission: {str(e)}"
            
    except Exception as e:
        return False, f"Error connecting to GitHub: {str(e)}"

# [Rest of your existing code remains the same until the submission part]

# In the submission tab, replace the submission handling with:
with tabs[1]:
    if st.button("Submit", type="primary"):
        if not name or not email:
            st.error("Please fill in both your Name and Email before submitting.")
        elif 'map_obj' not in st.session_state or 'distances' not in st.session_state:
            st.error("Please run your code and generate the map before submitting.")
        else:
            try:
                # Grade the submission
                from grades.grade1 import grade_submission
                score, breakdown = grade_submission(code)

                # Prepare submission dictionary
                submission = {
                    'Full name': name.strip(),
                    'email': email.strip(),
                    'student ID': student_id.strip() if student_id else 'N/A',
                    'assignment1': score
                }

                # Attempt to update GitHub
                with st.spinner('Submitting your assignment...'):
                    success, message = update_github_csv(submission)
                
                if success:
                    st.success(f"✅ Assignment submitted successfully! Your grade is: {score}/100")
                    st.balloons()
                else:
                    st.error(f"❌ Error during submission: {message}")
                    
            except Exception as e:
                st.error(f"❌ Error during submission: {str(e)}")
