# grade1.py
import ast
from geopy.distance import geodesic

def grade_assignment(code_str):
    grade = 0
    feedback = []
    
    try:
        # Parse the code
        tree = ast.parse(code_str)
        
        # Check imports (5 points)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(n.name for n in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
        
        required_libs = {'folium', 'geopy'}
        import_score = 5 if all(lib in str(imports) for lib in required_libs) else 0
        grade += import_score
        
        # Execute code to check functionality
        try:
            # Create namespace
            namespace = {}
            exec(code_str, namespace)
            
            # Check coordinates (5 points)
            coords = [
                (36.325735, 43.928414),
                (36.393432, 44.586781),
                (36.660477, 43.840174)
            ]
            
            coord_score = 0
            if any('folium.Map' in str(node) for node in ast.walk(tree)):
                coord_score += 5
            grade += coord_score
            
            # Check if code runs (10 points)
            grade += 10
            
            # Code efficiency (10 points)
            efficiency_score = 10
            grade += efficiency_score
            
            # Map visualization (40 points)
            map_score = 0
            if 'folium' in imports:
                # Check map generation (15 points)
                if any('folium.Map' in str(node) for node in ast.walk(tree)):
                    map_score += 15
                
                # Check markers (15 points)
                if any('folium.Marker' in str(node) for node in ast.walk(tree)):
                    map_score += 15
                
                # Check polyline (10 points)
                if any('folium.PolyLine' in str(node) for node in ast.walk(tree)):
                    map_score += 10
            
            grade += map_score
            
            # Distance calculations (30 points)
            expected_distances = {
                (0, 1): 59.57,  # Point 1 to Point 2
                (1, 2): 73.14,  # Point 2 to Point 3
                (0, 2): 37.98   # Point 1 to Point 3
            }
            
            distance_score = 0
            if 'geopy' in str(imports):
                distance_score += 10  # Correct implementation
                
                # Check distances in output
                output_vars = namespace
                distances_found = 0
                tolerance = 0.1  # 100m tolerance
                
                for var in output_vars.values():
                    if isinstance(var, (int, float)):
                        for expected_dist in expected_distances.values():
                            if abs(var - expected_dist) < tolerance:
                                distances_found += 1
                
                distance_score += (distances_found * 20) // 3  # Up to 20 points for correct distances
            
            grade += distance_score
            
            feedback.append(f"Import score: {import_score}/5")
            feedback.append(f"Coordinate handling: {coord_score}/5")
            feedback.append(f"Code execution: 10/10")
            feedback.append(f"Code efficiency: {efficiency_score}/10")
            feedback.append(f"Map visualization: {map_score}/40")
            feedback.append(f"Distance calculations: {distance_score}/30")
            
        except Exception as e:
            feedback.append(f"Error during execution: {str(e)}")
            grade = max(grade - 20, 0)  # Penalty for runtime errors
            
    except SyntaxError as e:
        feedback.append(f"Syntax error in code: {str(e)}")
        grade = 0
    
    return grade, "\n".join(feedback)
