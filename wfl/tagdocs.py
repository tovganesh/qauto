import os
import re
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK data (first-time only)
nltk.download("punkt")
nltk.download('punkt_tab')

# Define Tags
TAGS = {
    "finance": ["invoice", "payment", "amount", "bill", "tax"],
    "contact_info": ["phone", "email", "address", "contact", "fax"],
    "product_details": ["product", "item", "quantity", "price", "order"],
    "partnership": ["company", "firm"],
    "identity": ["pan", "dob", "aadhar", "passport"]
}

# Function to Tag Text Blocks
def tag_text_blocks(text, tags=TAGS):
    sentences = sent_tokenize(text)
    tagged_blocks = []

    for sentence in sentences:
        matched_tags = [
            tag for tag, keywords in tags.items() 
            if any(re.search(rf"\b{keyword}\b", sentence, re.IGNORECASE) for keyword in keywords)
        ]

        if matched_tags:
            tagged_blocks.append({
                "text": sentence.strip(),
                "tags": matched_tags
            })

    return tagged_blocks

# Process Text Files in a Directory
def process_text_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_dir, filename)

            try:
                with open(input_file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    tagged_blocks = tag_text_blocks(text)

                    output_file_path = os.path.join(output_dir, f"tagged_{filename}")
                    with open(output_file_path, "w", encoding="utf-8") as out_file:
                        for block in tagged_blocks:
                            out_file.write(f"Text: {block['text']}\n")
                            out_file.write(f"Tags: {', '.join(block['tags'])}\n")
                            out_file.write("-" * 80 + "\n")
                    
                    print(f"Processed: {filename}")
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example Usage
input_directory = "txt"
output_directory = "txtags"

process_text_files(input_directory, output_directory)
