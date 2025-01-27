from groq import Groq
import base64
import os

client = Groq()

image_analyst_sys_prompt = """You are an expert imagery analyst. You will be provided a composite image of an old image on the left side, and the new image on the right side, divided by a vertical white bar 100 pixels wide, and you will describe the differences between them. You must take into consideration what might be causing the changes (cloud cover, ground objects moving, etc.)"""

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_change(model_name="llama-3.2-11b-vision-preview"):
    print(f"Calling {model_name} to perform change detection")
    composite_images_folder = "composite_images"
    image_path = os.path.join(composite_images_folder, os.listdir(composite_images_folder)[0])
    print(image_path)
    encoded_image = encode_image(image_path)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                       "type": "text", "text": image_analyst_sys_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": 
                        {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        }
                    }
                ]
            }
        ],
        model=model_name,
    )
    response = chat_completion.choices[0].message.content
    print(response)
    return response