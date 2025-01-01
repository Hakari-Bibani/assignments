import ast
import pandas as pd
from geopy.distance import geodesic

def grade():
    # Read the latest submission
    df = pd.read_csv('grades/data_submission.csv')
    latest_submission = df.iloc[-1]
    code = latest_submission['code']
    
    total_points = 0
    
    # 1. Code Structure and Implementation (30 points)
    try:
        # Parse the code to check imports
        tree = ast.parse(code)
        imports = [node for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]
        required_libraries = ['folium', 'geopy']
        
        # Check imports (5 points)
        import_points = sum(any(lib in str(imp) for imp in imports) for lib in required_libraries) * 2.5
        total_points += import_points
        
        # Check coordinate handling (5 points)
        coordinates = [
            (36.325735, 43.928414),
            (36.393432, 44.586781),
            (36.660477, 43.840174)
        ]
        coord_points = 5 if all(str(coord) in code for coord in coordinates) else 0
        total_points += coord_points
        
        # Code runs without errors (10 points)
        try:
            exec(code)
            total_points += 10
        except:
            pass
        
        # Code efficiency (10 points) - basic check for clean code
        lines = code.split('\n')
        efficiency_points = 10 if len(lines) < 100 and not any(line.strip().startswith('print') for line in lines) else 5
        total_points += efficiency_points
        
    except:
        pass
    
    # 2. Map Visualization (40 points)
    try:
        # Check for map generation (15 points)
        if 'folium.Map' in code:
            total_points += 15
        
        # Check for markers (15 points)
        if 'folium.Marker' in code:
            total_points += 15
        
        # Check for polylines (10 points)
        if 'folium.PolyLine' in code:
            total_points += 10
            
    except:
        pass
    
    # 3. Distance Calculations (30 points)
    try:
        # Check for geodesic calculations (10 points)
        if 'geodesic' in code:
            total_points += 10
        
        # Check distance accuracy (20 points)
        correct_distances = {
            '1-2': 59.57,
            '2-3': 73.14,
            '1-3': 37.98
        }
        
        # Execute code and check output
        local_vars = {}
        exec(code, globals(), local_vars)
        
        for var_name, var_value in local_vars.items():
            if isinstance(var_value, (int, float)):
                # Check if the value is close to any correct distance
                for correct_dist in correct_distances.values():
                    if abs(var_value - correct_dist) < 0.1:
                        total_points += 6.67  # 20 points / 3 distances
                        
    except:
        pass
    
    # Update grade in CSV
    df.loc[df.index[-1], 'total'] = total_points
    df.to_csv('grades/data_submission.csv', index=False)
    
    return total_points
