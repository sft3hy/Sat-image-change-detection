import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import shutil
import regex as re
import numpy as np
from scipy.ndimage import zoom
import streamlit as st


def find_band_files(folder_path):
    """
    Groups files in the folder by their `_s` timestamp, associating them with bands C01, C02, and C03.
    """
    band_files = {}
    file_pattern = r"_s(\d+)"  # Regex to capture the `_s` timestamp

    # Iterate through files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".nc"):  # Only process .nc files
            match = re.search(file_pattern, file_name)
            if match:
                timestamp = match.group(1)  # Extract `_s` timestamp
                if timestamp not in band_files:
                    band_files[timestamp] = {}
                if "C01" in file_name:
                    band_files[timestamp]["C01"] = os.path.join(folder_path, file_name)
                elif "C02" in file_name:
                    band_files[timestamp]["C02"] = os.path.join(folder_path, file_name)
                elif "C03" in file_name:
                    band_files[timestamp]["C03"] = os.path.join(folder_path, file_name)
    return band_files

def resample_to_match(data, target_shape):
    """
    Resamples `data` to match `target_shape` using nearest-neighbor interpolation.
    """
    zoom_factors = [t / s for t, s in zip(target_shape, data.shape)]
    return zoom(data, zoom_factors, order=1)

def save_goes_images_png(band_files, timestamp):
    """
    Reads and renders a GOES-R ABI L1b radiance file (e.g., ABI-L1b-RadC).
    """
    try:
        # Open datasets for each band
        ds_c01 = xr.open_dataset(band_files["C01"])  # Blue
        ds_c02 = xr.open_dataset(band_files["C02"])  # Red
        ds_c03 = xr.open_dataset(band_files["C03"])  # Green (approximated)
        
        # Extract radiance data
        blue = ds_c01["Rad"].data
        red = ds_c02["Rad"].data
        green = ds_c03["Rad"].data
        
        # Resample all bands to match the highest resolution (smallest shape)
        target_shape = min(blue.shape, red.shape, green.shape)
        blue = resample_to_match(blue, target_shape)
        red = resample_to_match(red, target_shape)
        green = resample_to_match(green, target_shape)
        
        # Adjust green band for better true-color approximation
        green = 0.45 * red + 0.10 * blue + 0.45 * green
        
        # Normalize data to range [0, 1]
        blue = np.clip(blue / blue.max(), 0, 1)
        red = np.clip(red / red.max(), 0, 1)
        green = np.clip(green / green.max(), 0, 1)
        
        # Stack bands into an RGB image
        rgb_image = np.stack([red, green, blue], axis=-1)
        
        # Extract geolocation info from one dataset
        x = ds_c02["x"].data
        y = ds_c02["y"].data
        proj_info = ds_c02["goes_imager_projection"]
        
        # Set up satellite projection
        sat_proj = ccrs.Geostationary(
            central_longitude=proj_info.longitude_of_projection_origin,
            satellite_height=proj_info.perspective_point_height
        )
        
        # Plot true-color image
        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=sat_proj)
        img = ax.imshow(rgb_image, extent=(x.min(), x.max(), y.min(), y.max()),
                        origin="upper", transform=sat_proj)
        
        # Add coastlines and features
        ax.add_feature(cfeature.COASTLINE, edgecolor="white")
        ax.add_feature(cfeature.BORDERS, linestyle=":")
        ax.add_feature(cfeature.STATES, edgecolor="white")
        
        image_dir = "converted_to_pngs"
        
        # Save the plot to a PNG file
        filename = f"{timestamp}.png"
        plt.axis('off')
        plt.savefig(os.path.join(image_dir, filename), bbox_inches='tight', dpi=300, pad_inches=0)
        plt.close()
        print(f"Wrote file {filename}")
    
    except Exception as e:
        print(f"Error rendering image: {e}")

raw_nc_images_dir = ".raw_nc_images"
converted_to_pngs_dir = "converted_to_pngs"


def wipe_and_write_new_pngs():
    print("Writing new nc files to png")
    if os.path.exists(converted_to_pngs_dir):
        if os.path.exists(converted_to_pngs_dir):
            shutil.rmtree(converted_to_pngs_dir)
        os.makedirs(converted_to_pngs_dir)

    band_files_by_timestamp = find_band_files(raw_nc_images_dir)
    count = 1
    for timestamp, band_files in band_files_by_timestamp.items():
        with st.spinner(f"Converting image {count}/{len(band_files_by_timestamp.items())}"):
            if "C01" in band_files and "C02" in band_files and "C03" in band_files:
                print(f"Processing timestamp {timestamp}...")
                save_goes_images_png(band_files, timestamp)
        count += 1
