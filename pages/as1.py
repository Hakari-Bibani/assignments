import folium
from geopy.distance import geodesic
import json

def create_map_and_calculate_distances():
    # Define the coordinates
    coordinates = [
        (36.325735, 43.928414),  # Point 1
        (36.393432, 44.586781),  # Point 2
        (36.660477, 43.840174)   # Point 3
    ]
    
    # Create a map centered on the middle point
    center_lat = sum(coord[0] for coord in coordinates) / len(coordinates)
    center_lon = sum(coord[1] for coord in coordinates) / len(coordinates)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    
    # Add markers for each point
    for i, coord in enumerate(coordinates, 1):
        folium.Marker(
            coord,
            popup=f'Point {i}',
            icon=folium.Icon(color='red')
        ).add_to(m)
    
    # Calculate distances
    distances = {
        'Point 1 to Point 2': round(geodesic(coordinates[0], coordinates[1]).kilometers, 2),
        'Point 2 to Point 3': round(geodesic(coordinates[1], coordinates[2]).kilometers, 2),
        'Point 1 to Point 3': round(geodesic(coordinates[0], coordinates[2]).kilometers, 2)
    }
    
    # Save map to HTML
    map_path = 'output_map.html'
    m.save(map_path)
    
    return {
        'map_path': map_path,
        'distances': distances
    }

def run_assignment(student_code):
    """
    Runs and validates student submitted code.
    Returns a tuple of (success, output, error_message)
    """
    try:
        # Create a temporary namespace to execute student code
        namespace = {}
        exec(student_code, namespace)
        
        # Check if required functions exist
        required_functions = ['create_map', 'calculate_distances']
        for func in required_functions:
            if func not in namespace:
                return False, None, f"Missing required function: {func}"
        
        # Run student code and validate output
        student_map = namespace['create_map']()
        student_distances = namespace['calculate_distances']()
        
        # Validate against correct implementation
        correct_output = create_map_and_calculate_distances()
        
        # Compare distances (allowing for small differences due to calculation methods)
        for key in correct_output['distances']:
            if abs(student_distances[key] - correct_output['distances'][key]) > 0.1:
                return False, None, f"Incorrect distance calculation for {key}"
        
        return True, {
            'map': student_map,
            'distances': student_distances
        }, None
        
    except Exception as e:
        return False, None, str(e)

if __name__ == "__main__":
    # Test the reference implementation
    result = create_map_and_calculate_distances()
    print("Distances:", json.dumps(result['distances'], indent=2))
