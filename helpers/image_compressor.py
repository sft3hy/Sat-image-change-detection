from PIL import Image
import os

def shrink_image_to_target_size(image_path, target_size_bytes, output_path):
    """
    Resizes an image to reduce its file size to the target size.

    Parameters:
        image_path (str): Path to the input image.
        target_size_bytes (int): Desired file size in bytes (e.g., 3.9 MB = 3,900,000 bytes).
        output_path (str): Path to save the resized image.

    Returns:
        str: Path to the resized image.
    """
    # Open the image
    with Image.open(image_path) as img:
        quality = 95  # Start with high quality
        while True:
            # Save the image with the current quality level
            img.save(output_path, "JPEG", quality=quality)
            
            # Check the file size
            current_size = os.path.getsize(output_path)
            if current_size <= target_size_bytes or quality <= 5:
                break
            
            # Reduce quality iteratively
            quality -= 5

    return output_path

# Example usage
# image_path = "composite_images/composite_2025-01-28_10:18:22.200349_to_2025-01-28_10:18:14.369029.png"
# output_path = "resized_example.png"
# target_size_bytes = 3900000  # 3.9 MB

# resized_image = shrink_image_to_target_size(image_path, target_size_bytes, output_path)
# print(f"Resized image saved to: {resized_image}")
