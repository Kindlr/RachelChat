import openai
from decouple import config
from functions.database import get_recent_messages

# Retrieve Environment Variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

# OpenAI - Whisper
# Convert Audio to Text
def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        print(e)
        return None  # It's a good practice to return a value also in case of an exception, None in this case.

# OpenAI - ChatGPT
# Get Response to our Message
def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        message_text = response["choices"][0]["message"]["content"]  # Fixed the key access
        return message_text
    except Exception as e:
        print(e)
        return None  # Again, it's a good practice to return a value also in case of an exception, None in this case.
