import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import shutil
from datetime import datetime

def save_goes_images_png(file_path):
    """
    Reads and renders a GOES-R ABI L1b radiance file (e.g., ABI-L1b-RadC).
    """
    try:
        # Open the NetCDF file
        ds = xr.open_dataset(file_path)
        
        # Extract the radiance data
        radiance = ds['Rad'].data

        # Extract geolocation information
        x = ds['x'].data  # Scaled x-coordinates
        y = ds['y'].data  # Scaled y-coordinates
        proj_info = ds['goes_imager_projection']
        
        # Set up the satellite projection
        sat_proj = ccrs.Geostationary(
            central_longitude=proj_info.longitude_of_projection_origin,
            satellite_height=proj_info.perspective_point_height
        )
        
        # Plot the radiance data
        plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=sat_proj)
        im = ax.imshow(radiance, extent=(x.min(), x.max(), y.min(), y.max()),
                  origin='upper', cmap='gray', transform=sat_proj)
        
        # Add coastlines and features
        ax.add_feature(cfeature.COASTLINE, edgecolor='red')
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.STATES, edgecolor='blue')
        
        image_dir = "converted_to_pngs"
        
        # Save the plot to a PNG file
        filename = f"{datetime.now()}.png"
        plt.axis('off')
        plt.savefig(os.path.join(image_dir, filename), bbox_inches='tight', dpi=300, pad_inches=0)
        plt.close()
        print(f"Wrote file {filename}")
    
    except Exception as e:
        print(f"Error rendering image: {e}")

raw_nc_images_dir = "raw_nc_images"
converted_to_pngs_dir = "converted_to_pngs"


def wipe_and_write_new_pngs():
    print("Writing new nc files to png")
    if os.path.exists(converted_to_pngs_dir):
        if os.path.exists(converted_to_pngs_dir):
            shutil.rmtree(converted_to_pngs_dir)
        os.makedirs(converted_to_pngs_dir)

    for filename in os.listdir(raw_nc_images_dir):
        if filename.endswith(".nc"):
            file_path = os.path.join(raw_nc_images_dir, filename)
            save_goes_images_png(file_path)
