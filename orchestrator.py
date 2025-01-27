from llama_vision import analyze_change
from composite_image_creator import do_the_compositing
from goes_downloads import refresh_images_folder
from nc_to_png import wipe_and_write_new_pngs

# step 1: download 2 most recent images in nc format
# refresh_images_folder()

# step 2: save them as pngs
# wipe_and_write_new_pngs()

# step 3: create a composite with old one on the left
# do_the_compositing()

# step 4: analyze with llama vision 11 or 90b
analyze_change()