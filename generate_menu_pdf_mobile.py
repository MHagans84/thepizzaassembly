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
GOLD = HexColor('#D4A853')
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
    
    temp_path = '/tmp/circular_logo_mobile.png'
    output.save(temp_path, 'PNG')
    return temp_path

def draw_italian_divider(c, y, width):
    """Draw Italian flag divider"""
    bar_width = 40
    bar_height = 5
    start_x = (width - bar_width * 3) / 2
    
    c.setFillColor(ITALIAN_GREEN)
    c.rect(start_x, y, bar_width, bar_height, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.rect(start_x + bar_width, y, bar_width, bar_height, fill=1, stroke=0)
    c.setFillColor(ITALIAN_RED)
    c.rect(start_x + bar_width * 2, y, bar_width, bar_height, fill=1, stroke=0)

def create_mobile_menu_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'The-Pizza-Assembly-Menu.pdf')
    logo_path = os.path.join(script_dir, 'center logo.png')
    
    # Mobile-friendly size (narrower, taller - like a phone screen)
    page_width = 4.5 * inch
    page_height = 10 * inch
    
    c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
    
    # Background
    c.setFillColor(CREAM)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    
    margin = 20
    content_width = page_width - margin * 2
    y = page_height - 30
    
    # Logo (circular)
    logo_size = 90
    circular_logo = create_circular_logo(logo_path, logo_size * 2)
    c.drawImage(circular_logo, (page_width - logo_size) / 2, y - logo_size, 
                width=logo_size, height=logo_size, mask='auto')
    y -= logo_size + 10
    
    # Tagline
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Oblique", 14)
    c.drawCentredString(page_width / 2, y, "Neapolitan Style")
    y -= 16
    c.drawCentredString(page_width / 2, y, "Pizza")
    y -= 20
    
    # Divider
    draw_italian_divider(c, y, page_width)
    y -= 25
    
    # Pizza Kits Section
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_width / 2, y, "Pizza Kits")
    y -= 20
    
    def draw_pizza_card(c, y, name, desc, price_14, price_16):
        card_height = 80
        
        # Card background
        c.setFillColor(WHITE)
        c.roundRect(margin, y - card_height, content_width, card_height, 10, fill=1, stroke=0)
        
        # Item name (centered, large)
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(page_width / 2, y - 18, name)
        
        # Prices as text rows (like dough balls)
        price_y = y - 38
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica", 10)
        c.drawString(margin + 20, price_y, '14" Medium')
        c.setFillColor(ITALIAN_GREEN)
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(margin + content_width - 20, price_y, f'${price_14}')
        
        price_y -= 14
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica", 10)
        c.drawString(margin + 20, price_y, '16" Large')
        c.setFillColor(ITALIAN_RED)
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(margin + content_width - 20, price_y, f'${price_16}')
        
        # Description (centered, smaller)
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 7)
        desc_y = price_y - 14
        c.drawCentredString(page_width / 2, desc_y, desc[:60] + "...")
        
        return y - card_height - 10
    
    y = draw_pizza_card(c, y, "Margherita", 
        "San Marzano tomatoes, fresh mozzarella, Parmigiano Reggiano, Pecorino Romano, fresh basil. Includes fresh dough.",
        14, 16)
    
    y = draw_pizza_card(c, y, "Pepperoni",
        "Premium pepperoni, San Marzano tomatoes, fresh mozzarella, Parmigiano Reggiano, fresh basil. Includes fresh dough.",
        14, 16)
    
    y -= 5
    draw_italian_divider(c, y, page_width)
    y -= 25
    
    # Dough Balls Section
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_width / 2, y, "Dough Balls")
    y -= 14
    
    c.setFillColor(GRAY)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(page_width / 2, y, "48-hour cold fermented")
    y -= 20
    
    def draw_dough_card(c, y, title, subtitle, prices, color):
        card_height = 75
        
        # Card background
        c.setFillColor(WHITE)
        c.roundRect(margin, y - card_height, content_width, card_height, 10, fill=1, stroke=0)
        
        # Title
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(page_width / 2, y - 18, title)
        
        # Subtitle
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 9)
        c.drawCentredString(page_width / 2, y - 32, subtitle)
        
        # Prices
        price_y = y - 50
        for i, (size, price) in enumerate(prices):
            py = price_y - i * 16
            c.setFillColor(DARK_TEXT)
            c.setFont("Helvetica", 11)
            c.drawString(margin + 20, py, size)
            c.setFillColor(color)
            c.setFont("Helvetica-Bold", 12)
            c.drawRightString(margin + content_width - 20, py, price)
        
        return y - card_height - 10
    
    y = draw_dough_card(c, y, "Fresh", "Use same day", 
        [('14" Medium (300g)', '$4'), ('16" Large (400g)', '$6')], ITALIAN_GREEN)
    
    y = draw_dough_card(c, y, "Frozen", "Thaw overnight",
        [('14" Medium (300g)', '$4'), ('16" Large (400g)', '$6')], GOLD)
    
    y -= 5
    draw_italian_divider(c, y, page_width)
    y -= 18
    
    # Ingredients footer
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 7)
    c.drawCentredString(page_width / 2, y, "San Marzano Tomatoes • Fresh Mozzarella")
    y -= 10
    c.drawCentredString(page_width / 2, y, "Parmigiano Reggiano • Pecorino Romano • Fresh Basil")
    y -= 18
    
    # Footer
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_width / 2, y, "The Pizza Assembly")
    
    c.save()
    print(f"Mobile menu PDF created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_mobile_menu_pdf()
