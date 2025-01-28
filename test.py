import os
import streamlit as st 
from datetime import timedelta, datetime
import pytz

png_folder = "converted_to_pngs"
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
