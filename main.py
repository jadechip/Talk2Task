"""Talk2Task

Talk2Task simplifies tasks by dividing them into smaller subtasks and carrying out each step using a chosen tool. Leveraging one-shot prompting, it uses minimal input to generate structured responses, which are then converted into actionable commands. Essentially, it translates user-friendly conversation into command-line execution, making task management and system interactions intuitive and efficient.

"""

import re
import os
import subprocess
import openai

class Tool:
    def __init__(self, name):
        self.name = name

    def useTool(self, command):
        pass

class CommandExecutor(Tool):
    def __init__(self):
        super().__init__('CommandExecutor')

    def useTool(self, command):
        result = subprocess.run(command, capture_output=True, shell=True)
        return result.stdout

class FileCreator(Tool):
    def __init__(self):
        super().__init__('FileCreator')

    def useTool(self, command):
        os.makedirs(command, exist_ok=True)
        return f"Directory {command} created."

class CodeWriter(Tool):
    def __init__(self, filename):
        super().__init__('CodeWriter')
        self.filename = filename

    def useTool(self, code):
        with open(self.filename, 'w') as file:
            file.write(code)
        return f"File {self.filename} written."

class Talk2Task:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        self.tool_map = {
            'CommandExecutor': CommandExecutor(),
            'FileCreator': FileCreator(),
        }
        self.tool_prompts = {
            'CommandExecutor': 'CommandExecutor allows you to run shell commands. Use it by writing [CommandExecutor(your_command)].',
            'FileCreator': 'FileCreator lets you create a directory. Use it by writing [FileCreator(/path/to/directory)].',
        }

    def generate_llm_messages(self, query):
        tool_descriptions = '\n'.join([f'{name}: {desc}' for name, desc in self.tool_prompts.items()])
        messages = [
            {
                "role": "system",
                "content": f"""
                Based on the tools available to you ({tool_descriptions}), break down a given task or query into specific steps.
                For each step, specify the tool that should be used and the exact command that should be executed.
                Your response MUST be a JSON list of commands in the following format:
                [["ToolName", "Command1"], ["ToolName", "Command2"], ...]
                Do not provide any additional text or explanation in the response, only the JSON list of commands.
                Query:
                {query}
                """
            },
            {
                "role": "user",
                "content": query
            }
        ]
        return messages

    def interact_with_gpt(self, prompt):
        messages = self.generate_llm_messages(prompt)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=messages
        )
        response = completion.choices[0].message['content']
        print(f"Response: {response}")

        return response

    def parse_response(self, response):
        response = self.preprocess_response(response)

        patterns = [
            r'\["(\w+)"\s*,\s*"([^"]+)"\]',
            r'\[(\w+)\((.+)\)\]',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, response)
            if matches:
                break
        else:
            raise ValueError("Response does not contain a list of commands")

        commands = [(match[0], match[1]) for match in matches]

        return commands

    def preprocess_response(self, response):
        response = response.replace('\n', '')
        response = re.sub(r'\s+', ' ', response)
        return response.strip()

    def execute_commands(self, commands):
        results = []
        current_file = None
        for cmd in commands:
            tool, args = cmd
            if tool in self.tool_map:
                print(f"Executing command: {tool}({args})")
                result = self.tool_map[tool].useTool(args)
                print(f"Result: {result}\n")
                results.append((tool, args, result))
            else:
                raise Exception(f'Unknown command type: {tool}')
        return results

    def process_prompt(self, prompt, retry=3):
        try:
            response = self.interact_with_gpt(prompt)
            commands = self.parse_response(response)
            results = self.execute_commands(commands)
            return results
        except Exception as e:
            if retry > 0:
                print(f"Error encountered: {e}. Retrying...")
                return self.process_prompt(prompt, retry - 1)
            else:
                raise e

if __name__ == "__main__":
    # Initialize the library with your OpenAI API key
    lib = lib = Talk2Task("<OPENAI_API_KEY>")

    # Define a prompt that GPT-X will understand to create a directory
    prompt = "Write a bash script to download the PDF from this URL: https://arxiv.org/abs/2305.01257 and save it to the current local directory"

    # Process the prompt
    result = lib.process_prompt(prompt)

    # Print the result
    print(result)

    """Talk2Task breaks down a given task into a list of substasks, then executes each command using a selected tool."""
