import ast

def calculate_grade(code):
    """
    Calculate the grade for the assignment based on the submitted code.
    """
    grade = 0

    # Parse the code into an abstract syntax tree (AST)
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0  # Return 0 if the code has syntax errors

    # Check for required libraries
    required_libraries = ["folium", "geopy"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for lib in required_libraries:
                if lib in [n.name for n in node.names]:
                    grade += 5  # Award points for correct library imports

    # Check for coordinate handling
    if "COORDINATES" in code:
        grade += 5  # Award points for correct coordinate handling

    # Check for distance calculations
    if "geodesic" in code:
        grade += 10  # Award points for using geodesic function

    # Check for map visualization
    if "folium.Map" in code and "folium.Marker" in code:
        grade += 15  # Award points for correct map generation

    # Ensure the grade does not exceed 100
    return min(grade, 100)
