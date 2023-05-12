# Talk2Task
Talk2Task simplifies tasks by dividing them into smaller subtasks and carrying out each step using a chosen tool.
Leveraging one-shot prompting, it uses minimal input to generate structured responses, which are then converted into actionable commands. Essentially, it translates user-friendly conversation into command-line execution, making task management and system interactions intuitive and efficient.


## Usage

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jadechip/Talk2Task/blob/main/example.ipynb)


```
!pip install openai
```

```
# Initialize the library with your OpenAI API key
lib = Talk2Task("<OPENAI_API_KEY>")

# Define a prompt that GPT-X will understand to create a directory
prompt = "Write a bash script to download the PDF from this URL: https://arxiv.org/abs/2305.01257 and save it to the current local directory"

# Process the prompt
result = lib.process_prompt(prompt)

# Print the result
print(result)
```
