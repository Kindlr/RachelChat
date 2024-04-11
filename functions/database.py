# Import necessary libraries
import json
import random

# Function to get recent messages
def get_recent_messages():
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "You are working at a futuristic retail store, assisting customers. Your name is Rachel. The user is Amir. Keep your answers friendly and under 30 words."
    }

    messages = [learn_instruction]

    try:
        with open(file_name, "r") as user_file:
            data = json.load(user_file)
            messages.extend(data)
    except FileNotFoundError:
        pass  # If the file doesn't exist yet, it's okay. We'll create it in store_messages.
    except Exception as e:
        print(f"Failed to load messages: {e}")

    return messages

# Function to store messages
def store_messages(request_message, response_message):
    file_name = "stored_data.json"
    messages = get_recent_messages()[1:]  # Exclude the learn_instruction message

    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}

    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file
    try:
        with open(file_name, "w") as f:
            json.dump(messages, f)
    except Exception as e:
        print(f"Failed to save messages: {e}")

# Function to reset messages
def reset_messages():
    # Overwrite the current file with an empty JSON array
    open("stored_data.json", "w").write("[]")

# Creative Scenario:
# Rachel and Amir engage in a friendly chat at the futuristic retail store
store_messages("Hi Amir, how's your day going?", "Hey Rachel! It's great. The store is buzzing today. How about you?")
store_messages("I love the futuristic vibe here. What's your favorite feature of the store?", "I adore the holographic product displays. They're so eye-catching!")
store_messages("Have you tried the new VR shopping experience?", "Not yet, but I've heard it's amazing. Have you?")
store_messages("Not yet, but I'm curious. Maybe we should try it together after work?", "Sounds like a plan! Let's explore the virtual world of shopping together!")








