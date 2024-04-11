# uvicorn main:app --reload

# Main Imports
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# Custom Function Imports
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech  # corrected the typo 'funtions' to 'functions'

# Initiate App
app = FastAPI()

# CORS - origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000"
]

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check Health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}

# Reset Messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "Conversation reset"}

# Get audio
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    # Save file from Frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")  # Indentation fixed here
    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)
    
    # Guard: Ensure message decoded 
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")
    
    # Get ChatGPT Response
    chat_response = get_chat_response(message_decoded)

    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed to get chat response")
    
    # Store messages
    store_messages(message_decoded, chat_response)
    
    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)
    
    # Guard: Ensure audio output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response")
    
    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output
    
    # Return audio file 
    return StreamingResponse(iterfile(), media_type="application/octet-stream")  # Set the media type to audio/mpeg

# Uncomment the below lines if you want to run using the below command instead of uvicorn command
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)















