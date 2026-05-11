import os

def write_data_to_txt(data, filename):
    
    filename = f"research/{filename}.txt"
    
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            pass  # Create an empty file if it doesn't exist
    
    with open(filename, 'a') as file:
        for item in data:
            file.write(f"{item}\n")