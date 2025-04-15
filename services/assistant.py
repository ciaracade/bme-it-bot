import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Creates singular assistant instance that can do multiple tasks 
assistant = openai.beta.assistants.create(
    name="HelpdeskBot",
    instructions="You are a helpful assistant that categorizes IT support tickets, summarizes them, and suggests responses.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

# Print assistant ID into file for easy grabs
f = open('output.txt','w')
print("Assistant ID:", assistant.id, file = f)
f.close()
