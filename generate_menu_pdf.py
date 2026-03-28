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
GOLD = HexColor('#D4A853')
GRAY = HexColor('#666666')

def create_circular_logo(image_path, size=150):
    """Create a circular version of the logo"""
    img = Image.open(image_path).convert("RGBA")
    
    # Resize to square
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create circular mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply mask
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    # Save temp file
    temp_path = '/tmp/circular_logo.png'
    output.save(temp_path, 'PNG')
    return temp_path

def draw_italian_divider(c, y, width):
    """Draw Italian flag divider"""
    bar_width = 30
    bar_height = 4
    start_x = (width - bar_width * 3) / 2
    
    c.setFillColor(ITALIAN_GREEN)
    c.rect(start_x, y, bar_width, bar_height, fill=1, stroke=0)
    
    c.setFillColor(HexColor('#FFFFFF'))
    c.rect(start_x + bar_width, y, bar_width, bar_height, fill=1, stroke=0)
    
    c.setFillColor(ITALIAN_RED)
    c.rect(start_x + bar_width * 2, y, bar_width, bar_height, fill=1, stroke=0)

def create_menu_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'The-Pizza-Assembly-Menu.pdf')
    logo_path = os.path.join(script_dir, 'center logo.png')
    
    # Create PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Background
    c.setFillColor(CREAM)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Starting Y position
    y = height - 60
    
    # Logo (circular)
    logo_size = 120
    circular_logo = create_circular_logo(logo_path, logo_size * 2)  # Higher res
    logo_x = (width - logo_size) / 2
    c.drawImage(circular_logo, logo_x, y - logo_size, width=logo_size, height=logo_size, mask='auto')
    y -= logo_size + 15
    
    # Tagline
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Oblique", 14)
    c.drawCentredString(width / 2, y, "Authentic Neapolitan Style")
    y -= 18
    c.drawCentredString(width / 2, y, "Pizza")
    y -= 30
    
    # Divider
    draw_italian_divider(c, y, width)
    y -= 30
    
    # Pizza Kits Section
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "Pizza Kits")
    y -= 30
    
    # Menu items
    margin = 50
    card_width = width - margin * 2
    
    def draw_menu_item(c, y, name, desc, price_med, price_lg):
        card_height = 70
        
        # Card background
        c.setFillColor(HexColor('#FFFFFF'))
        c.roundRect(margin, y - card_height, card_width, card_height, 8, fill=1, stroke=0)
        
        # Item name
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin + 15, y - 22, name)
        
        # Prices
        c.setFillColor(ITALIAN_GREEN)
        c.setFont("Helvetica-Bold", 11)
        price_x = margin + card_width - 130
        c.roundRect(price_x, y - 26, 55, 20, 10, fill=1, stroke=0)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(price_x + 27.5, y - 21, price_med)
        
        c.setFillColor(ITALIAN_RED)
        c.roundRect(price_x + 60, y - 26, 55, 20, 10, fill=1, stroke=0)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(price_x + 87.5, y - 21, price_lg)
        
        # Description
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 10)
        c.drawString(margin + 15, y - 45, desc[:80])
        if len(desc) > 80:
            c.drawString(margin + 15, y - 57, desc[80:])
        
        return y - card_height - 12
    
    y = draw_menu_item(c, y, "Margherita", 
        "San Marzano tomatoes, fresh mozzarella, Parmigiano Reggiano, Pecorino Romano, fresh basil. Includes fresh dough.",
        '14" $15', '16" $20')
    
    y = draw_menu_item(c, y, "Pepperoni",
        "Premium pepperoni, San Marzano tomatoes, fresh mozzarella, Parmigiano Reggiano, fresh basil. Includes fresh dough.",
        '14" $15', '16" $20')
    
    y -= 10
    
    # Divider
    draw_italian_divider(c, y, width)
    y -= 30
    
    # Dough Balls Section
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "Dough Balls")
    y -= 18
    
    c.setFillColor(GRAY)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2, y, "48-hour cold fermented")
    y -= 25
    
    # Dough cards side by side
    card_w = (card_width - 15) / 2
    card_h = 90
    
    def draw_dough_card(c, x, y, title, subtitle, prices, color):
        # Card background
        c.setFillColor(HexColor('#FFFFFF'))
        c.roundRect(x, y - card_h, card_w, card_h, 8, fill=1, stroke=0)
        
        # Title
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x + card_w / 2, y - 20, title)
        
        # Subtitle
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 9)
        c.drawCentredString(x + card_w / 2, y - 34, subtitle)
        
        # Prices
        c.setFont("Helvetica", 11)
        for i, (size, price) in enumerate(prices):
            py = y - 52 - i * 18
            c.setFillColor(DARK_TEXT)
            c.drawString(x + 15, py, size)
            c.setFillColor(color)
            c.setFont("Helvetica-Bold", 11)
            c.drawRightString(x + card_w - 15, py, price)
            c.setFont("Helvetica", 11)
    
    draw_dough_card(c, margin, y, "Fresh", "Use same day", 
        [('14" (250g)', '$5'), ('16" (350g)', '$6')], ITALIAN_GREEN)
    
    draw_dough_card(c, margin + card_w + 15, y, "Frozen", "Thaw overnight",
        [('14" (250g)', '$4'), ('16" (350g)', '$5')], GOLD)
    
    y -= card_h + 25
    
    # Divider
    draw_italian_divider(c, y, width)
    y -= 25
    
    # Ingredients footer
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    ingredients = "San Marzano Tomatoes • Fresh Mozzarella • Parmigiano Reggiano • Pecorino Romano • Fresh Basil"
    c.drawCentredString(width / 2, y, ingredients)
    y -= 25
    
    # Footer
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, y, "The Pizza Assembly")
    
    c.save()
    print(f"PDF created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_menu_pdf()
