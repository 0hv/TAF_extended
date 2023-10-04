import os
import logging
from datetime import datetime
import re
import fnmatch

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def is_excluded(path, excluded_directories, excluded_file_types):
    """Check if the given path should be excluded based on the provided exclusion lists."""

    # Check if path matches any of the excluded directories
    for excluded_dir in excluded_directories:
        if re.search(excluded_dir, path):
            return True

    # Check if file type is in the excluded file types
    if os.path.isfile(path):
        for excluded_type in excluded_file_types:
            if fnmatch.fnmatch(path, excluded_type):
                return True

    return False


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

        # Check if the directory should be excluded
        if is_excluded(directory, excluded_dirs, excluded_file_types):
            logging.info(f"Excluding directory: {directory}")
            subdirectories[:] = []  # Don't traverse its subdirectories
            continue

        logging.info(f"Adding directory to tree structure: {directory}")
        tree_structure.append(f"{indent}|-- {dir_name}/")

        for file in files:
            file_path = os.path.join(directory, file)
            if not is_excluded(file_path, excluded_dirs, excluded_file_types):
                logging.info(f"Adding file to tree structure: {file_path}")
                tree_structure.append(f"{indent}|   |-- {file}")

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

    # Define directories to exclude
    excluded_directories = {r".idea$", r"venv$", r"venv\\Lib", r"venv\\Scripts", r".*stock.*"}
    excluded_file_types = {"*.txt", "*.db"}

    # Retrieve the tree structure
    tree_structure = retrieve_tree_structure(project_path, excluded_dirs=excluded_directories, excluded_file_types=excluded_file_types)

    # Generate the content of the markdown file
    markdown_content = "\n".join(tree_structure) + "\n\n"

    # Add the content of the files
    for directory, subdirectories, files in os.walk(project_path):

        # Check if the current directory matches any of the excluded directory patterns
        if any(re.search(excluded_dir, directory) for excluded_dir in excluded_directories):
            continue  # Skip the current directory and move to the next one

        # Iterate through all the files in the current directory
        for file in files:

            # Skip files with a '.db' extension
            if file.endswith('.db'):
                continue

            # Construct the full path of the current file
            file_path = os.path.join(directory, file)

            # Open the file in read mode with UTF-8 encoding, ignoring any read errors
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Read all lines from the file
                lines = f.readlines()
                # Combine the lines into a single string
                content = ''.join(lines)

            # Check if the file path does not contain ".idea"
            if r".idea" not in file_path:
                # Add the file content to the markdown content with formatting
                markdown_content += f"{'=' * 50}\n===== {file} ({file_path.replace(project_path, '')}) =====\n{'=' * 50}\n\n{content}\n\n"
            else:
                # Skip the content of files from the .idea directory
                continue

    # Save the markdown content to a file
    output_directory = os.path.join(project_path, 'framework_utils', 'scrapper', 'data_stock')
    create_output_directory(output_directory)
    current_date = datetime.now().strftime('%d%m%y_%H%M%S')
    output_filename = f"scrapage_{current_date}.md"
    output_file_path = os.path.join(output_directory, output_filename)

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        logging.info(f"Markdown file stored in '{output_file_path}'.")
    except Exception as e:
        logging.error(f"Error writing to the file {output_file_path}. Error: {e}")



if __name__ == "__main__":
    main()
