from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from model_generate_reponse import generate_response
from read_pdf import process_pdf

app = FastAPI()

# Define the request schema for prompt-based requests
class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask/")
async def ask_model(request: PromptRequest):
    prompt = request.prompt
    # Generate a response using the model
    response_text = generate_response(prompt)
    return {"response": response_text}
