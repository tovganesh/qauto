import os
import sys
import ollama
import json

# Check command-line arguments
if len(sys.argv) < 4:
    print("Usage: python summarize.py <input_directory> <output_directory> <output_format>")
    print("output_format: text or json")
    sys.exit(1)

# Initialize the Ollama client
client = ollama.Client()

# Directories and format
input_directory = sys.argv[1]
output_directory = sys.argv[2]
output_format = sys.argv[3].lower()

# Ensure valid output format
if output_format not in ["text", "json"]:
    print("Error: Output format must be 'text' or 'json'.")
    sys.exit(1)

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Model and options
model_name = "llama3.2:1b"
options = {
    "temperature": 0.1,
    "top_k": 10,
    "top_p": 0.9,
    "seed": 2025,
    "repeat_penalty": 1.1,
    "num_predict": 1024,
}

# Function to summarize a file
def summarize_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    prompt = f"Summarize the following text, provide the output as {output_format}:\n\n{content}"
    
    response = client.generate(
        model=model_name,
        prompt=prompt,
        options=options
    )
    return response["response"]

# Iterate through files and summarize
for filename in os.listdir(input_directory):
    file_path = os.path.join(input_directory, filename)
    if os.path.isfile(file_path) and filename.endswith(".txt"):
        summary = summarize_file(file_path)

        # Define output file extension
        file_extension = "json" if output_format == "json" else "txt"
        summary_file_path = os.path.join(
            output_directory, f"{os.path.splitext(filename)[0]}_summary.{file_extension}"
        )

        # Save summary to the output directory
        with open(summary_file_path, "w", encoding="utf-8") as summary_file:
            if output_format == "json":
                # Ensure JSON is saved in a proper format
                try:
                    summary_data = json.loads(summary)
                    json.dump(summary_data, summary_file, indent=4, ensure_ascii=False)
                except json.JSONDecodeError:
                    summary_file.write(summary)  # Fallback in case of malformed JSON
            else:
                summary_file.write(summary)

        print(f"Summary saved for {filename} at {summary_file_path}")
