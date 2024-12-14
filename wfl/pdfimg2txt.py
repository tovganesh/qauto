import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import os

# Extract text from a single PDF file
def extract_text_from_pdf(file_path):
    pdf_text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                pdf_text += text if text else ""
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return pdf_text

# Extract text from images in the PDF
def extract_text_from_images(file_path):
    ocr_text = ""
    try:
        images = convert_from_path(file_path, dpi=300)
        for image in images:
            text = pytesseract.image_to_string(image, lang="eng")
            ocr_text += text + "\n"
    except Exception as e:
        print(f"Error extracting images from {file_path}: {e}")
    return ocr_text

# Convert PDFs in a directory
def convert_pdfs_to_text(directory, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            
            # Extract text from both PDF content and images
            text = extract_text_from_pdf(file_path)
            image_text = extract_text_from_images(file_path)

            # Combine results
            complete_text = text + "\n" + image_text

            output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(complete_text)
                print(f"Extracted text saved to {output_file}")

# Example usage
input_dir = "pdf"
output_dir = "txt"

convert_pdfs_to_text(input_dir, output_dir)
