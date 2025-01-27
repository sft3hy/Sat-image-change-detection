import boto3
import schedule
import time
from datetime import datetime, timedelta
import pytz
import os
import shutil

# AWS S3 bucket and region info for GOES-R data
BUCKET_NAME = "noaa-goes18"
REGION_NAME = "us-east-1"

# GOES-R specific parameters
PRODUCT = "ABI-L1b-RadC"  # Example: radiance
bands = ["C01", "C02", "C03"]
SAVE_DIR = "raw_nc_images/"  # Local directory to save images

# Initialize the S3 client
s3 = boto3.client("s3", region_name=REGION_NAME)

def refresh_images_folder():
    print("Downloading new nc files from s3")
    # Wipe the images folder
    if os.path.exists(SAVE_DIR):
        shutil.rmtree(SAVE_DIR)
    os.makedirs(SAVE_DIR)

    # Calculate the current timestamp and round to the nearest 15 minutes
    now = datetime.now(pytz.UTC)
    nearest_15_min = now - timedelta(minutes=now.minute % 15, seconds=now.second, microseconds=now.microsecond)

    # Format the path for the NOAA GOES-R data
    year = nearest_15_min.strftime("%Y")
    day_of_year = nearest_15_min.strftime("%j")  # Day of year
    hour = nearest_15_min.strftime("%H")
    
    # Example file path pattern in the S3 bucket
    s3_prefix = f"{PRODUCT}/{year}/{day_of_year}/{hour}/"
    print(s3_prefix)
    try:
        # List objects in the S3 bucket for the given prefix
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=s3_prefix)
        # print(response)
        if "Contents" in response:
            # Find the 2 latest files (by modification time)
            latest_files = sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)[:2]
            for i, latest_file in enumerate(latest_files):
                file_key = latest_file["Key"]
                
                # Download the file
                file_name = file_key.split("/")[-1]
                local_file_path = f"{SAVE_DIR}{file_name}"
                s3.download_file(BUCKET_NAME, file_key, local_file_path)
                
                print(f"Downloaded: {local_file_path}")
        else:
            print("No files found for the current time window.")
    except Exception as e:
        print(f"Error fetching GOES image: {e}")

# Schedule the task every 15 minutes
# fetch_goes_image()
# schedule.every(15).minutes.do(fetch_goes_image)

# print("Starting the GOES-R image feed...")
# while True:
#     schedule.run_pending()
#     time.sleep(1)
