import pandas as pd
from pathlib import Path

def grade_submission(submission):
    # Initialize scoring
    total_points = 0
    max_points = 100
    
    # Grade Question 1 (50 points)
    q1_keywords = ['general-purpose', 'web development', 'data analysis', 'artificial intelligence']
    q1_answer = submission['q1_answer'].lower()
    
    for keyword in q1_keywords:
        if keyword in q1_answer:
            total_points += 12.5  # Up to 50 points for Q1
    
    # Grade Question 2 (50 points)
    q2_answer = submission['q2_answer'].lower()
    if 'print' in q2_answer and 'hello, world' in q2_answer:
        if 'def' in q2_answer and '():' in q2_answer:  # Check for function definition
            total_points += 50
        else:
            total_points += 25  # Partial credit for correct print statement
    
    # Calculate final grade
    final_grade = min(total_points, max_points)  # Cap at max points
    
    # Save grade
    save_grade(submission, final_grade)
    
def save_grade(submission, grade):
    # Create grades directory if it doesn't exist
    Path('grades').mkdir(exist_ok=True)
    
    # Prepare grade data
    grade_data = {
        'student_name': submission['student_name'],
        'student_id': submission['student_id'],
        'week': submission['week'],
        'grade': grade,
        'timestamp': pd.Timestamp.now()
    }
    
    # Save to CSV
    csv_path = 'grades/data_submission.csv'
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        df = pd.DataFrame()
    
    # Update or append grade
    if len(df) > 0:
        mask = (df['student_id'] == grade_data['student_id']) & (df['week'] == grade_data['week'])
        if mask.any():
            df.loc[mask, 'grade'] = grade_data['grade']
            df.loc[mask, 'timestamp'] = grade_data['timestamp']
        else:
            df = pd.concat([df, pd.DataFrame([grade_data])], ignore_index=True)
    else:
        df = pd.DataFrame([grade_data])
    
    df.to_csv(csv_path, index=False)
