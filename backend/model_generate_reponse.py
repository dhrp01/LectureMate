from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer at startup to avoid repeated loading
model_name = "path/to/your-fine-tuned-model"  # Replace with the path or name of your model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Move model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_response(prompt: str, max_length: int = 100):
    # Tokenize and move the input to the correct device
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2
        )

    # Decode the output and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
