import os
import logging
from datetime import datetime

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def retrieve_tree_structure(root_path, excluded_dirs=None, excluded_file_types=None):
    if excluded_dirs is None:
        excluded_dirs = set()
    if excluded_file_types is None:
        excluded_file_types = set()

    tree_structure = []

    for directory, subdirectories, files in os.walk(root_path):
        level = directory.replace(root_path, '').count(os.sep)
        indent = '|   ' * level
        dir_name = os.path.basename(directory)

        # Check if the directory name contains "stock"
        if "stock" in dir_name.lower():
            tree_structure.append(f"{indent}|-- {dir_name}/")
            continue

        if dir_name not in excluded_dirs:
            tree_structure.append(f"{indent}|-- {dir_name}/")
            for file in files:
                if not any(file.endswith(file_type) for file_type in excluded_file_types):
                    tree_structure.append(f"{indent}|   |-- {file}")

        # Update the list of subdirectories by excluding specific directories.
        # This line iterates through the subdirectories in the current directory being processed.
        # If a subdirectory is not present in the 'excluded_dirs' set, it is included in the new list.
        # This effectively removes directories matching the names in 'excluded_dirs'.
        subdirectories[:] = [d for d in subdirectories if d not in excluded_dirs]

    return tree_structure

def get_project_path():
    current_path = os.path.abspath(__file__)

    while current_path != os.path.dirname(current_path):  # Until we reach the root
        current_path = os.path.dirname(current_path)
        if os.path.basename(current_path) == "TAA_extended":
            break

    return current_path

def create_output_directory(directory):
    if not os.path.exists(directory):
        logging.info(f"The directory {directory} does not exist. Attempting to create...")
        try:
            os.makedirs(directory)
            logging.info(f"Directory {directory} successfully created.")
        except Exception as e:
            logging.error(f"Error creating the directory {directory}. Error: {e}")

def main():
    project_path = get_project_path()
    print(project_path)

    # Define directories to exclude
    excluded_directories = {".idea", "venv", "Lib", "Scripts"}  # Add the specific directories to exclude

    # Define file types to exclude (e.g., "*.txt")
    excluded_file_types = {"*.txt"}

    # Retrieve the tree structure
    result = retrieve_tree_structure(project_path, excluded_dirs=excluded_directories, excluded_file_types=excluded_file_types)

    # Path to the output directory (data_stock in the same directory as the script)
    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_stock')
    create_output_directory(output_directory)

    # Create the filename with the requested format
    script_name = os.path.basename(__file__).split('.')[0]
    current_date = datetime.now().strftime('%d%m%y_%H%M')
    output_filename = f"{script_name}_{current_date}.txt"

    output_file_path = os.path.join(output_directory, output_filename)
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for line in result:
                f.write(f"{line}\n")
        logging.info(f"Tree structure stored in '{output_file_path}'.")
    except Exception as e:
        logging.error(f"Error writing to the file {output_file_path}. Error: {e}")

    # Check for the file's existence
    if os.path.exists(output_file_path):
        logging.info(f"The file was successfully created at: {output_file_path}")
    else:
        logging.error(f"The file was not found at: {output_file_path}")
        if not os.path.exists(output_directory):
            logging.error(f"The probable reason is that the destination directory {output_directory} does not exist.")

if __name__ == "__main__":
    main()
