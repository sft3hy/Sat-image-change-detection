from groq import Groq
import base64
import os
import streamlit as st
from helpers.image_compressor import shrink_image_to_target_size
import streamlit as st

client = Groq()

image_analyst_sys_prompt = """You are an expert satellite imagery analyst. You will be provided a composite satellite image of the Southern West 
coast of the United States and the Pacific Ocean, where the one day old image on the left side, and the current image on the right side, divided by a vertical white 
bar 100 pixels wide, and you will describe the differences between them. You must take into consideration what might be causing the changes (cloud cover, etc.)"""

def encode_image(image_path):
  with st.spinner("Encoding image..."):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
  


def stream_groq(stream):
    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text is not None and type(text) != "int":
            yield text

def analyze_change(model_name="llama-3.2-11b-vision-preview"):
    print(f"Calling {model_name} to perform change detection")
    composite_images_folder = "composite_images"
    image_path = os.path.join(composite_images_folder, os.listdir(composite_images_folder)[0])

    output_path = "composite_images/shrunk.png"
    target_size_bytes = 3900000  # 3.9 MB
    shrink_image_to_target_size(image_path, target_size_bytes, output_path)

    encoded_image = encode_image(output_path)
    stream = client.chat.completions.create(
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
        stream=True
    )
    
    with st.chat_message("ai"):
        response = st.write_stream(stream_groq(stream))
    response = stream
    return response

# analyze_change()