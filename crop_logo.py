from PIL import Image
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, 'PZA Logo - HQ.png')
output_path = os.path.join(script_dir, 'PZA Logo - Cropped.png')

# Open the image
img = Image.open(logo_path)
width, height = img.size

print(f"Original size: {width} x {height}")

# Crop off the bottom portion (the tagline text and Italian flag bars)
# Need to remove the Italian flag bars and "Premium Ingredients" text
crop_height = int(height * 0.68)  # Keep top 68% - just above the flag bars

cropped = img.crop((0, 0, width, crop_height))
cropped.save(output_path, 'PNG')

print(f"Cropped size: {width} x {crop_height}")
print(f"Saved to: {output_path}")
