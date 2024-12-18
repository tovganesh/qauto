import os
import sys
import ollama

# Initialize the Ollama client
client = ollama.Client()

# Directories and question
summary_directory = sys.argv[1]
question = sys.argv[2]

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

# Read all summary files
def read_all_summaries(directory):
    summaries = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith("_summary.txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                summaries.append(file.read())
    return " ".join(summaries)

# Ask a question based on summaries
def answer_question(question, context):
    prompt = f"Based on the following summaries, answer the question in detail:\n\n{context}\n\nQuestion: {question}\nAnswer:"
    
    response = client.generate(
        model=model_name,
        prompt=prompt,
        options=options
    )

    return response["response"]

# Main execution
if __name__ == "__main__":
    summaries = read_all_summaries(summary_directory)
    if summaries.strip():
        answer = answer_question(question, summaries)
        print(f"Question: {question}\nAnswer: {answer}")
    else:
        print("No summaries found in the specified directory.")
