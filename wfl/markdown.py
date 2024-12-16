import os
from markitdown import MarkItDown

def process_files_in_directory(directory):
    # Supported file extensions
    supported_extensions = ('.xlsx', '.pdf', '.doc', '.txt')

    # Initialize MarkItDown
    markitdown = MarkItDown()

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(supported_extensions):
            file_path = os.path.join(directory, filename)

            try:
                result = markitdown.convert(file_path)
                print(f"Processed {filename}:\n")
                print(result.text_content)
                print("-" * 80)

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python process_files.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"{directory_path} is not a valid directory.")
        sys.exit(1)

    process_files_in_directory(directory_path)
