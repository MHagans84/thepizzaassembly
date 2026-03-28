from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw
import os

CREAM = HexColor('#F5F1E6')
ITALIAN_GREEN = HexColor('#008C45')

def create_circular_logo(image_path, size=150):
    """Create a circular version of the logo"""
    img = Image.open(image_path).convert("RGBA")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    temp_path = '/tmp/circular_logo_sticker.png'
    output.save(temp_path, 'PNG')
    return temp_path

def draw_sticker(c, x, y, sticker_size, logo_path):
    """Draw a single circular logo sticker"""
    
    # Circular background
    c.setFillColor(CREAM)
    c.setStrokeColor(ITALIAN_GREEN)
    c.setLineWidth(2)
    c.circle(x + sticker_size/2, y + sticker_size/2, sticker_size/2, fill=1, stroke=1)
    
    # Logo (slightly smaller than the circle)
    logo_size = sticker_size * 0.85
    circular_logo = create_circular_logo(logo_path, int(logo_size * 2))
    offset = (sticker_size - logo_size) / 2
    c.drawImage(circular_logo, x + offset, y + offset, 
                width=logo_size, height=logo_size, mask='auto')

def create_sticker_sheet():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'Logo-Stickers.pdf')
    logo_path = os.path.join(script_dir, 'center logo.png')
    
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter
    
    # Sticker size (2 inch diameter circles - good for sealing bags)
    sticker_size = 2 * inch
    
    # Margins and spacing
    margin_x = 0.5 * inch
    margin_y = 0.5 * inch
    spacing = 0.25 * inch
    
    # Calculate grid
    cols = int((page_width - 2 * margin_x + spacing) / (sticker_size + spacing))
    rows = int((page_height - 2 * margin_y + spacing) / (sticker_size + spacing))
    
    count = 0
    for row in range(rows):
        for col in range(cols):
            x = margin_x + col * (sticker_size + spacing)
            y = page_height - margin_y - (row + 1) * sticker_size - row * spacing
            
            draw_sticker(c, x, y, sticker_size, logo_path)
            count += 1
    
    c.save()
    print(f"Logo stickers created: {output_path}")
    print(f"Grid: {cols} columns x {rows} rows = {count} stickers per page")
    return output_path

if __name__ == "__main__":
    create_sticker_sheet()
