import os
import sys
import ollama

# Initialize the Ollama client
client = ollama.Client()

# Directories
input_directory = sys.argv[1]
output_directory = sys.argv[2]

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Model and options
model_name = "llama3.2:1b"
options = {
    "temperature": 0.5,
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
    
    prompt = f"Summarize the following text, give the output as json:\n\n{content}"
    
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

        # Save summary to the output directory
        summary_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_summary.txt")
        with open(summary_file_path, "w", encoding="utf-8") as summary_file:
            summary_file.write(summary)
        
        print(f"Summary saved for {filename} at {summary_file_path}")
