import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")
# Eleven Labs
# Convert Text to Speech
def convert_text_to_speech(message):
    
    # Define Data(Body)
    body = {
        "text": message,
        "voice settings": {
            "stability": 0,
            "similarity_boost": 0, 
        }
    }

    # Define voice
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"

    # Constructing headers and endpoint for the request
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"  # Corrected the content type
    }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"  # Corrected URL typo (.lo to .io)

    # Sending the request to the Eleven Labs API
    try:
        response = requests.post(endpoint, headers=headers, json=body)
        
        # Handling a successful response
        if response.status_code == 200:
            return response.content  # Returning the audio content
        
        # Handling an error response
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Message: {response.text}")
            return None

    except Exception as e:
        # Handling any exceptions that occur during the request
        print(f"Error: {str(e)}")
        return None  # Returning None in case of an error


