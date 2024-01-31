import os
import requests

os.environ['API_TOKEN'] = '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'
API_TOKEN = os.environ["API_TOKEN"] 
headers = {"Authorization": f"Bearer {API_TOKEN}"}
#API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
#API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
#API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"

def query(prompt):
    payload = {
        "inputs": prompt,
        "parameters":{
            "max_new_tokens": 100,
            "temperature": 0.6,
            "top_p": 0.9,
            "do_sample": False,
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['generated_text']