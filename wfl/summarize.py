import os
import sys
import ollama

# Initialize the Ollama client
client = ollama.Client()

# Directory containing text files
directory = sys.argv[1]

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
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path) and filename.endswith(".txt"):
        summary = summarize_file(file_path)
        print(f"Summary of {filename}:\n{summary}\n{'-'*80}")
