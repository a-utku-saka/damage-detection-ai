from dotenv import load_dotenv
import os
import json
import base64
import requests
from openai import OpenAI

from utils.utils import _get_prompt

# OpenAI API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

class DamageDetection:  # New name instead of the old DetectFood
  
    def __init__(self):
        pass
    
    # Function to convert image to base64 format
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            return base64_image

    # Cargo damage detection function
    def analyze_damage(self, image_path1, image_path2, language):
        # Convert images to base64 string
        base64_image1 = self.encode_image(image_path1)
        base64_image2 = self.encode_image(image_path2)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        # Create Prompt
        system_prompt = _get_prompt("detect_damage") 
        system_prompt = system_prompt.replace("{{language}}", language)
        print(system_prompt)

        # JSON data to be sent to the API
        payload = {
            "model": "gpt-4o",  # Correct model name
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": system_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image1}"
                            }
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image2}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000,
            "temperature": 0,
            "response_format": { "type": "json_object" }

        }

        # Send request to API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        # Process response
        if response.status_code == 200:
            response_data = response.json()
            
            # Parse content from OpenAI
            content = response_data['choices'][0]['message']['content']
            content = json.loads(content)  # Convert to JSON format
            
            usage = response_data['usage']
            
            return content, usage
        else:
            print("Hata oluştu:", response.status_code, response.text)
            return None, None
