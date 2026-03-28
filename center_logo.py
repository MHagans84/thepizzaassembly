from PIL import Image
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, 'no tagline logo.png')
output_path = os.path.join(script_dir, 'no tagline logo centered.png')

# Open the image
img = Image.open(logo_path)
width, height = img.size

print(f"Original size: {width} x {height}")

# The logo has extra space at top ("THE" text) and bottom (Italian flag bars)
# We want to crop to center the pizza graphic better
# Crop from top and bottom to center the main pizza image

top_crop = int(height * 0.12)  # Remove some top space
bottom_crop = int(height * 0.12)  # Remove some bottom space

cropped = img.crop((0, top_crop, width, height - bottom_crop))

# Make it square by taking the center
new_width, new_height = cropped.size
if new_width != new_height:
    size = min(new_width, new_height)
    left = (new_width - size) // 2
    top = (new_height - size) // 2
    cropped = cropped.crop((left, top, left + size, top + size))

cropped.save(output_path, 'PNG')

print(f"Centered size: {cropped.size[0]} x {cropped.size[1]}")
print(f"Saved to: {output_path}")
