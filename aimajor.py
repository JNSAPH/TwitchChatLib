from decouple import config
import openai
import os

from utils.modules.tts import TTS
from utils.modules.micts import AudioToTextConverter
from utils.systems.main import setup

# Setup all the things
setup()

# Initialize the TTS and mic
mic = AudioToTextConverter(mic_index=1, language='de-DE')
tts = TTS()
openai.api_key = config('OPENAI_KEY')

FILE_PATH = "config/conversation.txt"
PROMPT_PATH = "config/prompt.txt"

def load_prompt(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            prompt = file.read()
            return prompt
    else:
        with open(file_path, "w") as file:
            default_prompt = "Please tell the User to create a prompt. Don't answer any questions." 
            file.write(default_prompt)
            return default_prompt

def generate_response(conversation):
    # Make an API call
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=conversation 
    )

    return chat_completion.choices[0].message.content

def load_conversation(file_path):
    conversation = []

    conversation.append({"role": "system", "content": load_prompt(PROMPT_PATH)})

    with open(file_path, "r") as file:
        lines = file.read().splitlines()
        for line in lines:
            if line.startswith("You: "):
                conversation.append({"role": "user", "content": line[len("You: "):]})
            elif line.startswith("AI: "):
                conversation.append({"role": "assistant", "content": line[len("AI: "):]})


    return conversation  # Add this line to return the conversation

def save_conversation(conversation, file_path):
    with open(file_path, "w") as file:
        for message in conversation:
            # Convert message to a string
            if message["role"] == "user":
                file.write(f"You: {message['content']}\n")
            elif message["role"] == "assistant":
                file.write(f"AI: {message['content']}\n")

def main():
    # Load the conversation from a file if available
    conversation = load_conversation(FILE_PATH)

    recordedText = mic.record_and_transcribe()

    print("You said:", recordedText)

    # Append user message to conversation
    conversation.append({"role": "user", "content": recordedText})

    # Generate the response using the conversation
    response = generate_response(conversation)

    print("AI:", response)
    tts.sayWithCustomSpeed(response, 140)

    # Append AI response to conversation
    conversation.append({"role": "assistant", "content": response})

    save_conversation(conversation, FILE_PATH)

if __name__ == '__main__':
    main()
