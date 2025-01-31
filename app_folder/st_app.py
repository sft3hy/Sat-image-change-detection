import streamlit as st
import os
from helpers.llama_vision import analyze_change
from helpers.composite_image_creator import do_the_compositing
from helpers.goes_downloads import refresh_images_folder
from helpers.nc_to_png import wipe_and_write_new_pngs
from datetime import datetime, timedelta
import pytz

st.subheader("Compare today's and yesterday's satellite imagery", divider=True)


col1, col2, col3 = st.columns(3)
with col2:
    do_workflow = st.button("Order imagery")

# Initialize session state variables
if "png_files" not in st.session_state:
    st.session_state["png_files"] = []
if "model_name" not in st.session_state:
    st.session_state["model_name"] = "llama-3.2-11b-vision-preview"
if "change_analysis" not in st.session_state:
    st.session_state["change_analysis"] = ""

# Sidebar for model selection
with st.sidebar:
    st.session_state["model_name"] = st.selectbox(
        "Vision model for image comparison:",
        options=["llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview"],
        index=0,
    )

def parse_goes_timestamp(timestamp):
    year = int(timestamp[:4])
    day_of_year = int(timestamp[4:7])
    hour = int(timestamp[7:9])
    minute = int(timestamp[9:11])
    second = int(timestamp[11:13])
    dt_utc = datetime(year, 1, 1) + timedelta(days=day_of_year - 1, hours=hour, minutes=minute, seconds=second)
    dt_utc = pytz.utc.localize(dt_utc)
    est = pytz.timezone('US/Eastern')
    dt_est = dt_utc.astimezone(est)
    return dt_est.strftime('%Y-%m-%d %H:%M:%S')

png_folder = "converted_to_pngs"


if do_workflow:
    st.session_state["change_analysis"] = ""
    with st.spinner("Downloading NetCDF files from AWS..."):
        refresh_images_folder()
    with st.spinner("Converting files to PNG format..."):
        wipe_and_write_new_pngs()
        st.session_state["png_files"] = [
            os.path.join(png_folder, file)
            for file in os.listdir(png_folder)
            if os.path.isfile(os.path.join(png_folder, file))
        ]

# Display the images if they exist in session state
if st.session_state["png_files"]:
    png_files = st.session_state["png_files"]
    col1, col2 = st.columns(2)
    if len(png_files) > 1:
        older = png_files[0]
        newer = png_files[1]
        if png_files[0] > png_files[1]:
            older = png_files[1]
            newer = png_files[0]
        with col1:
            st.image(
                older,
                caption=f"NOAA GOES-18 image taken at {parse_goes_timestamp(os.path.basename(older).split('.')[0])} EST",
            )
        with col2:
            st.image(
                newer,
                caption=f"NOAA GOES-18 image taken at {parse_goes_timestamp(os.path.basename(newer).split('.')[0])} EST",
            )
        with st.spinner("Creating composite image..."):
            do_the_compositing()
        st.subheader("Change Detection")
        if st.session_state["change_analysis"] != "":
            st.write(st.session_state["change_analysis"])
        else:
            st.session_state["change_analysis"] = analyze_change(model_name=st.session_state["model_name"])
