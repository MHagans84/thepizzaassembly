from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw
import os

# Colors
ITALIAN_RED = HexColor('#C8102E')
ITALIAN_GREEN = HexColor('#008C45')
CREAM = HexColor('#F5F1E6')
DARK_TEXT = HexColor('#2C2C2C')
GRAY = HexColor('#666666')
WHITE = HexColor('#FFFFFF')

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
    
    temp_path = '/tmp/circular_logo_instr.png'
    output.save(temp_path, 'PNG')
    return temp_path

def draw_italian_divider(c, x, y, width):
    """Draw Italian flag divider"""
    bar_width = 20
    bar_height = 2
    start_x = x + (width - bar_width * 3) / 2
    
    c.setFillColor(ITALIAN_GREEN)
    c.rect(start_x, y, bar_width, bar_height, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.rect(start_x + bar_width, y, bar_width, bar_height, fill=1, stroke=0)
    c.setFillColor(ITALIAN_RED)
    c.rect(start_x + bar_width * 2, y, bar_width, bar_height, fill=1, stroke=0)

def draw_instruction_card(c, x, y, card_width, card_height, logo_path):
    """Draw a single instruction card"""
    
    # Card background
    c.setFillColor(CREAM)
    c.roundRect(x, y, card_width, card_height, 8, fill=1, stroke=0)
    
    # Border
    c.setStrokeColor(ITALIAN_RED)
    c.setLineWidth(1.5)
    c.roundRect(x, y, card_width, card_height, 8, fill=0, stroke=1)
    
    center_x = x + card_width / 2
    current_y = y + card_height - 12
    
    # Logo (small)
    logo_size = 30
    circular_logo = create_circular_logo(logo_path, logo_size * 2)
    c.drawImage(circular_logo, center_x - logo_size/2, current_y - logo_size, 
                width=logo_size, height=logo_size, mask='auto')
    current_y -= logo_size + 5
    
    # Title
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(center_x, current_y, "Pizza Instructions")
    current_y -= 10
    
    draw_italian_divider(c, x, current_y, card_width)
    current_y -= 10
    
    # Steps
    steps = [
        ("1. Rest", "Remove dough from fridge 1-2 hrs before."),
        ("2. Stretch", "Push from center out on semolina."),
        ("3. Top", "Add sauce, cheese, toppings."),
        ("4. Bake", "450°F, bottom rack, 10 min."),
    ]
    
    for title, desc in steps:
        c.setFillColor(ITALIAN_GREEN)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(x + 8, current_y, title)
        current_y -= 8
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 6)
        c.drawString(x + 8, current_y, desc)
        current_y -= 10
    
    current_y += 2
    draw_italian_divider(c, x, current_y, card_width)
    current_y -= 10
    
    # Pro tip
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(center_x, current_y, "Pro Tip:")
    current_y -= 8
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(center_x, current_y, "Preheat pan/stone for crispy bottom!")
    current_y -= 10
    
    # Social
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica", 5)
    c.drawCentredString(center_x, current_y, "@thepizzaassembly")

def create_instruction_card_sheet():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'Pizza-Instruction-Cards.pdf')
    logo_path = os.path.join(script_dir, 'center logo.png')
    
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter
    
    # Card dimensions (2.5" x 3.5" - same as kit labels)
    card_width = 2.5 * inch
    card_height = 3.5 * inch
    
    # Margins and spacing
    margin_x = 0.5 * inch
    margin_y = 0.5 * inch
    spacing_x = 0.25 * inch
    spacing_y = 0.25 * inch
    
    # Calculate grid
    cols = int((page_width - 2 * margin_x + spacing_x) / (card_width + spacing_x))
    rows = int((page_height - 2 * margin_y + spacing_y) / (card_height + spacing_y))
    
    count = 0
    for row in range(rows):
        for col in range(cols):
            x = margin_x + col * (card_width + spacing_x)
            y = page_height - margin_y - (row + 1) * card_height - row * spacing_y
            
            draw_instruction_card(c, x, y, card_width, card_height, logo_path)
            count += 1
    
    c.save()
    print(f"Instruction cards created: {output_path}")
    print(f"Grid: {cols} columns x {rows} rows = {count} cards per page")
    return output_path

if __name__ == "__main__":
    create_instruction_card_sheet()
