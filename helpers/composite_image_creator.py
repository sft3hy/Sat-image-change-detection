import os
from PIL import Image
import shutil
import streamlit as st

composite_images_dir = "composite_images"
SEPARATION_PIXELS = 100

def create_composite_image(image1, image2):
    st.write("Creating composite image")

    if os.path.exists(composite_images_dir):
        if os.path.exists(composite_images_dir):
            shutil.rmtree(composite_images_dir)
        os.makedirs(composite_images_dir)
    
    image1_date = int(os.path.basename(image1).split('.')[0])
    image2_date = int(os.path.basename(image2).split('.')[0])

    if image1_date < image2_date:
        older_image = Image.open(image1)
        newer_image = Image.open(image2)
    else:
        older_image = Image.open(image2)
        newer_image = Image.open(image1)

    max_height = max(older_image.height, newer_image.height)
    older_image = older_image.resize((older_image.width, max_height))
    newer_image = newer_image.resize((newer_image.width, max_height))

    composite_image = Image.new('RGB', (older_image.width + newer_image.width + SEPARATION_PIXELS, max_height), (0, 0, 0))
    composite_image.paste(older_image, (0, 0))
    composite_image.paste(newer_image, (older_image.width + SEPARATION_PIXELS, 0))

    white_bar = Image.new('RGB', (SEPARATION_PIXELS, max_height), (255, 255, 255))
    composite_image.paste(white_bar, (older_image.width, 0))

    file_path = f"composite_images/composite_{str(image2_date).replace(' ', '_')}_to_{str(image1_date).replace(' ', '_')}.png"
    composite_image.save(file_path)
    return file_path


converted_to_pngs_dir = "converted_to_pngs"

def do_the_compositing():
    files = [os.path.join(converted_to_pngs_dir, f) for f in os.listdir(converted_to_pngs_dir) if os.path.isfile(os.path.join(converted_to_pngs_dir, f))]
    create_composite_image(files[0], files[1])