import streamlit as st

st.markdown("""
# Satellite Imagery Change Detection Workflow
## About the developer
            
Hey! I'm Sam and I like to make hobby projects like this. Check out my [personal website](https://sft3hy.github.io/sam-townsend). If you have any questions or need help, feel free to email me - smaueltown@gmail.com

---
## Project Overview
This project enables the detection of changes in satellite imagery using NOAA's GOES-18 data. The workflow involves downloading recent satellite images, processing them into a composite format, and analyzing the differences using a language model. The primary components of the project are designed for real-time, automated imagery processing and analysis.


## Key Modules and Functionality

### **1. helpers/composite_image_creator.py**
Handles the creation of composite images by combining two satellite images side-by-side with a separating white bar.

- **Key Features:**
  - Compares images based on file creation time.
  - Resizes images to the same height for alignment.
  - Generates a single composite image with a clear separation bar.

- **Core Function:** `create_composite_image(image1, image2)`

---

### **2. helpers/goes_downloads.py**
Facilitates the download of recent NOAA GOES-18 satellite images in NetCDF format from an AWS S3 bucket.

- **Key Features:**
  - Fetches images from NOAA's GOES-18 S3 bucket based on the current time.
  - Handles different satellite bands (e.g., M6C01, M6C02, M6C03).
  - Downloads and stores files locally for further processing.

- **Core Function:** `refresh_images_folder()`

---

### **3. helpers/nc_to_png.py**
Processes the downloaded NetCDF files and converts them into PNG images suitable for visual analysis.

- **Key Features:**
  - Extracts and normalizes radiance data from multiple satellite bands.
  - Merges bands into true-color RGB images.
  - Resamples data to maintain uniform resolution across bands.
  - Adds geographic overlays, such as coastlines and borders.

- **Core Function:** `wipe_and_write_new_pngs()`

---

### **4. helpers/llama_vision.py**
Performs change detection on composite images using a pretrained large language model.

- **Key Features:**
  - Encodes the composite image as a Base64 string for analysis.
  - Sends the image to a language model for descriptive analysis of detected changes.
  - Provides insights into cloud cover, object movement, and other environmental changes.

- **Core Function:** `analyze_change(model_name="llama-3.2-11b-vision-preview")`

---

### **5. app_folder/st_app.py**
A Streamlit-based user interface that integrates the above components into a cohesive workflow.

- **Key Features:**
  - Provides buttons to initiate the workflow.
  - Displays downloaded PNG images side-by-side with timestamps.
  - Triggers composite image creation and change detection analysis.

- **Core Workflow:**
  1. **Download recent satellite images** from NOAA GOES-18.
  2. **Convert NetCDF files to PNG** format.
  3. **Display images and generate a composite.**
  4. **Analyze changes** in the composite image using the language model.

---

## Workflow Overview
1. **Download Recent Imagery:** 
   - Connects to NOAA's AWS S3 bucket and fetches the most recent satellite images for specified bands.
2. **Convert NetCDF to PNG:**
   - Processes raw data to generate true-color images.
3. **Create Composite Image:**
   - Combines two PNG images for direct comparison.
4. **Analyze Changes:**
   - Uses a vision-enabled language model to describe differences in the images.

---

## Example Usage
1. Run the Streamlit app:
   ```bash
   streamlit run st.py


""")


