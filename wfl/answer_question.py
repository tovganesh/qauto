import os
import sys
import ollama

from pathlib import Path

# Initialize the Ollama client
client = ollama.Client()

# Directories and question
summary_directory = sys.argv[1]
question = sys.argv[2]

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

# Read summaries with filenames
def read_all_summaries(directory):
    summaries = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith("_summary.txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                summaries[filename] = file.read()
    return summaries

# Ask a question and get references
def answer_question(question, summaries):
    referenced_files = []
    detailed_answer = ""

    for filename, summary in summaries.items():
        prompt = f"""
Based on the following summary, answer the question in detail:
Summary: {summary}

Question: {question}
Answer:
"""
        response = client.generate(
            model=model_name,
            prompt=prompt.strip(),
            options=options
        )

        answer = response["response"].strip()
        
        # Consider answers only if they are meaningful
        if answer and answer.lower() != "i don't know":
            detailed_answer += f"From {filename}:\n{answer}\n\n"
            referenced_files.append(filename)

    return detailed_answer.strip(), referenced_files

def get_relevant_files(question, directory="."):
    keywords = question.lower().split()  # Simple keyword extraction
    relevant_files = []

    for file in Path(directory).glob("**/*.*"):
        if any(keyword in file.name.lower() for keyword in keywords):
            relevant_files.append(file)
    
    return relevant_files

# Main execution
if __name__ == "__main__":
    summaries = read_all_summaries(summary_directory)
    
    if summaries:
        answer, references = answer_question(question, summaries)
        if answer:
            print(f"Question: {question}\n")
            print(f"Answer:\n{answer}\n")
            print("References:")
            relevant_refs = get_relevant_files(question, summary_directory)
            for ref in relevant_refs:
                print(f" - {ref}")
        else:
            print("The question could not be answered based on the provided summaries.")
    else:
        print("No summaries found in the specified directory.")
