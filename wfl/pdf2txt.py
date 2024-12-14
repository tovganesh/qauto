import os
import sys
import PyPDF2

# Extract text from a single PDF file
def extract_text_from_pdf(file_path):
    pdf_text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                pdf_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return pdf_text

# Convert PDFs in a directory
def convert_pdfs_to_text(directory, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            text = extract_text_from_pdf(file_path)

            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
                print(f"Extracted text saved to {output_file}")

# Example usage
input_dir = sys.argv[1]
output_dir = sys.argv[2]

convert_pdfs_to_text(input_dir, output_dir)
