import boto3
from datetime import datetime, timedelta
import pytz
import os
import shutil
import regex as re
import streamlit as st

# AWS S3 bucket and region info for GOES-R data
BUCKET_NAME = "noaa-goes18"
REGION_NAME = "us-east-1"

# GOES-R specific parameters
PRODUCT = "ABI-L1b-RadC"  # Example: radiance
SAVE_DIR = ".raw_nc_images/"  # Local directory to save images
BANDS = ["M6C01", "M6C02", "M6C03"]
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Initialize the S3 client
s3 = boto3.client("s3", region_name=REGION_NAME, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,)

def download_from_response(response):
    # st.write(response['Contents'])
    most_recent_files = {}

    for item in response['Contents']:
        key = item['Key']
        for band in BANDS:
            if band in key:
                # If we don't have a record for this band or the current item is more recent
                if band not in most_recent_files or item['LastModified'] > most_recent_files[band]['LastModified']:
                    most_recent_files[band] = item
    for band, file_info in most_recent_files.items():
        file_name = file_info['Key'].split("/")[-1]
        local_file_path = f"{SAVE_DIR}{file_name}"
        s3.download_file(BUCKET_NAME, file_info['Key'], local_file_path)    
        st.write(f"Downloaded: {local_file_path}")

def refresh_images_folder():
    st.write("Downloading new nc files from s3")
    # Wipe the images folder
    if os.path.exists(SAVE_DIR):
        shutil.rmtree(SAVE_DIR)
    os.makedirs(SAVE_DIR)

    # Calculate the current timestamp and round to the nearest 10 minutes
    now = datetime.now(pytz.UTC)
    nearest_15_min = now - timedelta(minutes=now.minute % 10, seconds=now.second, microseconds=now.microsecond)

    yesterday = now - timedelta(days=1)
    s3_prefix_yesterday = yesterday.replace(hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)
    year_yesterday = s3_prefix_yesterday.strftime("%Y")
    day_of_year_yesterday = s3_prefix_yesterday.strftime("%j")  # Day of year
    hour_yesterday = s3_prefix_yesterday.strftime("%H")

    # Format the path for the NOAA GOES-R data
    year = nearest_15_min.strftime("%Y")
    day_of_year = nearest_15_min.strftime("%j")  # Day of year
    hour = nearest_15_min.strftime("%H")

    # Example file path pattern in the S3 bucket
    s3_prefix = f"{PRODUCT}/{year}/{day_of_year}/{hour}/"
    s3_prefix_yesterday = f"{PRODUCT}/{year_yesterday}/{day_of_year_yesterday}/{hour_yesterday}/"
    st.write(s3_prefix)
    try:
        # List objects in the S3 bucket for the given prefix
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=s3_prefix)
        yesterday_response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=s3_prefix_yesterday)
        if "Contents" in response:
            with st.spinner(f"Downloading today's image"):
                download_from_response(response)
            with st.spinner(f"Downloading yesterday's image"):
                download_from_response(yesterday_response)
        else:
            st.write("No files found for the current time window, trying earlier...")
            s3_prefix = '/'.join(s3_prefix.split('/')[:-1] + [str(int(s3_prefix.split('/')[-1]) - 1)])
            st.write(f"NEW S3 PREFIX: {s3_prefix}")
            st.write(s3_prefix)
            st.write()

            response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=s3_prefix)
            with st.spinner(f"Downloading today's image"):
                download_from_response(response)
            with st.spinner(f"Downloading yesterday's image"):
                download_from_response(yesterday_response)
    except Exception as e:
        st.write(f"Error fetching GOES image: {e}")