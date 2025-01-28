import streamlit as st
import os
from helpers.llama_vision import analyze_change
from helpers.composite_image_creator import do_the_compositing
from helpers.goes_downloads import refresh_images_folder
from helpers.nc_to_png import wipe_and_write_new_pngs
from datetime import datetime, timedelta
import pytz

st.subheader("Compare today's and yesterday's satellite imagery")

with st.sidebar:
    selected_model = st.selectbox(
            "Vision model for image comparison:",
            options = ["llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview"],
            index=0,
        )


def parse_goes_timestamp(timestamp):
    # Extract the year, day of year, hour, minute, and second
    year = int(timestamp[:4])
    day_of_year = int(timestamp[4:7])
    hour = int(timestamp[7:9])
    minute = int(timestamp[9:11])
    second = int(timestamp[11:13])
    
    # Convert to a datetime object in UTC
    dt_utc = datetime(year, 1, 1) + timedelta(days=day_of_year - 1, hours=hour, minutes=minute, seconds=second)
    dt_utc = pytz.utc.localize(dt_utc)  # Localize to UTC
    
    # Convert to Eastern Standard Time (EST)
    est = pytz.timezone('US/Eastern')
    dt_est = dt_utc.astimezone(est)
    return dt_est.strftime('%Y-%m-%d %H:%M:%S')
png_files = ''
png_folder = "converted_to_pngs"
do_workflow = st.button("Order imagery")
workflow_pressed = False
if do_workflow:
    workflow_pressed = True
    with st.spinner("Downloading NetCDF files from AWS..."):
        refresh_images_folder()
    with st.spinner("Converting files to PNG format..."):
        wipe_and_write_new_pngs()
        png_files = [os.path.join("converted_to_pngs", file) for file in os.listdir(png_folder) if os.path.isfile(os.path.join(png_folder, file))]
    col1, col2 = st.columns(2)
    if png_files is not [] and len(png_files) > 1:
        older = png_files[0]
        newer = png_files[1]
        if png_files[0] > png_files[1]:
            older = png_files[1]
            newer = png_files[0]
        with col1:
            st.image(png_files[-1], caption=f"NOAA GOES-18 image taken at {parse_goes_timestamp(older.split('/')[-1].split('.')[0])} EST")
        with col2:
            st.image(png_files[-2], caption=f"NOAA GOES-18 image taken at {parse_goes_timestamp(newer.split('/')[-1].split('.')[0])} EST")
        with st.spinner("Creating composite image..."):
            do_the_compositing()
        st.subheader("Change Detection")
        analyze_change(model_name=selected_model)