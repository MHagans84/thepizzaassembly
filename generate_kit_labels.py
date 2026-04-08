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
    
    temp_path = '/tmp/circular_logo_kit.png'
    output.save(temp_path, 'PNG')
    return temp_path

def draw_kit_label(c, x, y, label_width, label_height, logo_path):
    """Draw a single pizza kit label"""
    
    # Label background
    c.setFillColor(CREAM)
    c.roundRect(x, y, label_width, label_height, 8, fill=1, stroke=0)
    
    # Border
    c.setStrokeColor(ITALIAN_GREEN)
    c.setLineWidth(1.5)
    c.roundRect(x, y, label_width, label_height, 8, fill=0, stroke=1)
    
    center_x = x + label_width / 2
    current_y = y + label_height - 15
    
    # Logo (small)
    logo_size = 40
    circular_logo = create_circular_logo(logo_path, logo_size * 2)
    c.drawImage(circular_logo, center_x - logo_size/2, current_y - logo_size, 
                width=logo_size, height=logo_size, mask='auto')
    current_y -= logo_size + 8
    
    # Product name
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(center_x, current_y, "Pizza Kit")
    current_y -= 14
    
    # Business info
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(center_x, current_y, "The Pizza Assembly")
    current_y -= 10
    
    c.setFont("Helvetica", 7)
    c.setFillColor(GRAY)
    c.drawCentredString(center_x, current_y, "4016 Brazelton Way")
    current_y -= 9
    c.drawCentredString(center_x, current_y, "615-476-2345")
    current_y -= 12
    
    # Ingredients section
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(center_x, current_y, "Ingredients:")
    current_y -= 9
    
    c.setFont("Helvetica", 6)
    c.setFillColor(GRAY)
    
    # Dough ingredients
    c.drawCentredString(center_x, current_y, "Dough: Wheat Flour, Water, Salt, Yeast")
    current_y -= 8
    
    # Sauce ingredients
    c.drawCentredString(center_x, current_y, "Sauce: San Marzano Tomatoes,")
    current_y -= 8
    c.drawCentredString(center_x, current_y, "Olive Oil, Garlic, Salt, Basil")
    current_y -= 8
    
    # Cheese ingredients
    c.drawCentredString(center_x, current_y, "Cheese: Mozzarella,")
    current_y -= 8
    c.drawCentredString(center_x, current_y, "Parmigiano, Pecorino Romano")
    current_y -= 10
    
    # Storage note
    c.setFillColor(ITALIAN_GREEN)
    c.setFont("Helvetica-Oblique", 5.5)
    c.drawCentredString(center_x, current_y, "Keep refrigerated. Use within 2 days.")

def create_kit_label_sheet():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'Pizza-Kit-Labels.pdf')
    logo_path = os.path.join(script_dir, 'center logo.png')
    
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter
    
    # Label dimensions (2.5" x 3.5" - fits nicely on card stock)
    label_width = 2.5 * inch
    label_height = 3.5 * inch
    
    # Margins and spacing
    margin_x = 0.5 * inch
    margin_y = 0.5 * inch
    spacing_x = 0.25 * inch
    spacing_y = 0.25 * inch
    
    # Calculate grid
    cols = int((page_width - 2 * margin_x + spacing_x) / (label_width + spacing_x))
    rows = int((page_height - 2 * margin_y + spacing_y) / (label_height + spacing_y))
    
    count = 0
    for row in range(rows):
        for col in range(cols):
            x = margin_x + col * (label_width + spacing_x)
            y = page_height - margin_y - (row + 1) * label_height - row * spacing_y
            
            draw_kit_label(c, x, y, label_width, label_height, logo_path)
            count += 1
    
    c.save()
    print(f"Pizza kit labels created: {output_path}")
    print(f"Grid: {cols} columns x {rows} rows = {count} labels per page")
    return output_path

if __name__ == "__main__":
    create_kit_label_sheet()
