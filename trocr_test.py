import requests
import re

#API_URL = "https://api-inference.huggingface.co/models/microsoft/trocr-large-handwritten"
#API_URL = "https://api-inference.huggingface.co/models/microsoft/trocr-large-printed"
#API_URL = "https://api-inference.huggingface.co/models/DunnBC22/trocr-large-printed-cmc7_tesseract_MICR_ocr"
#API_URL = "https://api-inference.huggingface.co/models/fahmiaziz/finetune-donut-cord-v2.5"
API_URL = "https://api-inference.huggingface.co/models/jinhybr/OCR-Donut-CORD"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

if __name__ == "__main__":
  response_json = query("documents/Doctor-Note-2.jpg")
  print(response_json)
  print("------------------------------------------------------------------------------------")
  updated_txt = re.sub(r"<(\"[^\"]*\"|'[^']*'|[^'\">])*>", "", response_json[0]['generated_text']).strip() 
  print(updated_txt)