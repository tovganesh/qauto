import ollama

# Initialize Ollama API
client = ollama.Client()

# Function to load text from a file
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Define file path
file_path = 'extended_ship_activity_log.txt'

# Load text from file
text_input = load_text(file_path)

# Query LLaMA 3.2 using Ollama
response = client.generate(
    model="llama3.2:1b",
    prompt=text_input
)

# Print the response
print(response["response"])
