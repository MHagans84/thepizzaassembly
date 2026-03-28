from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw
import os

# Colors
ITALIAN_RED = HexColor('#C8102E')
ITALIAN_GREEN = HexColor('#008C45')
CREAM = HexColor('#F5F1E6')
DARK_TEXT = HexColor('#2C2C2C')
GRAY = HexColor('#666666')

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
    
    temp_path = '/tmp/circular_logo_label.png'
    output.save(temp_path, 'PNG')
    return temp_path

def draw_label(c, x, y, label_width, label_height, logo_path, product_name, size_info):
    """Draw a single label at the specified position"""
    
    # Label background
    c.setFillColor(CREAM)
    c.roundRect(x, y, label_width, label_height, 8, fill=1, stroke=0)
    
    # Border
    c.setStrokeColor(ITALIAN_GREEN)
    c.setLineWidth(1.5)
    c.roundRect(x, y, label_width, label_height, 8, fill=0, stroke=1)
    
    center_x = x + label_width / 2
    current_y = y + label_height - 12
    
    # Logo (small)
    logo_size = 35
    circular_logo = create_circular_logo(logo_path, logo_size * 2)
    c.drawImage(circular_logo, center_x - logo_size/2, current_y - logo_size, 
                width=logo_size, height=logo_size, mask='auto')
    current_y -= logo_size + 6
    
    # Product name
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(center_x, current_y, product_name)
    current_y -= 10
    
    # Size info
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica", 7)
    c.drawCentredString(center_x, current_y, size_info)
    current_y -= 12
    
    # Business name
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(center_x, current_y, "The Pizza Assembly")
    current_y -= 9
    
    # Address & Phone
    c.setFont("Helvetica", 6)
    c.setFillColor(GRAY)
    c.drawCentredString(center_x, current_y, "4016 Brazelton Way")
    current_y -= 8
    c.drawCentredString(center_x, current_y, "615-476-2345")
    current_y -= 10
    
    # Ingredients
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(center_x, current_y, "Ingredients: Wheat Flour, Water, Salt, Yeast")
    current_y -= 8
    
    # 48-hour fermented note
    c.setFillColor(ITALIAN_GREEN)
    c.setFont("Helvetica-Oblique", 5)
    c.drawCentredString(center_x, current_y, "48-Hour Cold Fermented")

def create_label_sheet():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'Dough-Ball-Labels.pdf')
    logo_path = os.path.join(script_dir, 'center logo.png')
    
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter
    
    # Label dimensions (2" x 2.5" - fits standard round container lids)
    label_width = 2 * inch
    label_height = 2.5 * inch
    
    # Margins and spacing
    margin_x = 0.5 * inch
    margin_y = 0.5 * inch
    spacing_x = 0.25 * inch
    spacing_y = 0.25 * inch
    
    # Calculate grid
    cols = int((page_width - 2 * margin_x + spacing_x) / (label_width + spacing_x))
    rows = int((page_height - 2 * margin_y + spacing_y) / (label_height + spacing_y))
    
    # Product variations
    products = [
        ("Fresh Dough Ball", "250g - 14\" Medium"),
        ("Fresh Dough Ball", "350g - 16\" Large"),
        ("Frozen Dough Ball", "250g - 14\" Medium"),
        ("Frozen Dough Ball", "350g - 16\" Large"),
    ]
    
    product_idx = 0
    
    for row in range(rows):
        for col in range(cols):
            x = margin_x + col * (label_width + spacing_x)
            y = page_height - margin_y - (row + 1) * label_height - row * spacing_y
            
            product_name, size_info = products[product_idx % len(products)]
            draw_label(c, x, y, label_width, label_height, logo_path, product_name, size_info)
            product_idx += 1
    
    c.save()
    print(f"Labels created: {output_path}")
    print(f"Grid: {cols} columns x {rows} rows = {cols * rows} labels per page")
    return output_path

if __name__ == "__main__":
    create_label_sheet()
