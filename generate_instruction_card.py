from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw
import qrcode
import os

# Colors
ITALIAN_RED = HexColor('#C8102E')
ITALIAN_GREEN = HexColor('#008C45')
CREAM = HexColor('#F5F1E6')
DARK_TEXT = HexColor('#2C2C2C')
GRAY = HexColor('#666666')
LIGHT_GRAY = HexColor('#999999')

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
    
    temp_path = '/tmp/circular_logo_card.png'
    output.save(temp_path, 'PNG')
    return temp_path

def create_qr_code(url, filename):
    """Generate QR code for a URL"""
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="#F5F1E6")
    path = f'/tmp/{filename}.png'
    img.save(path)
    return path

def draw_italian_divider(c, y, width):
    """Draw Italian flag divider"""
    bar_width = 25
    bar_height = 3
    start_x = (width - bar_width * 3) / 2
    
    c.setFillColor(ITALIAN_GREEN)
    c.rect(start_x, y, bar_width, bar_height, fill=1, stroke=0)
    c.setFillColor(HexColor('#FFFFFF'))
    c.rect(start_x + bar_width, y, bar_width, bar_height, fill=1, stroke=0)
    c.setFillColor(ITALIAN_RED)
    c.rect(start_x + bar_width * 2, y, bar_width, bar_height, fill=1, stroke=0)

def create_instruction_card():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'Pizza-Instructions.pdf')
    logo_path = os.path.join(script_dir, 'center logo.png')
    
    # Create QR codes
    instagram_qr = create_qr_code('https://www.instagram.com/thepizzaassembly/', 'instagram_qr')
    youtube_qr = create_qr_code('https://www.youtube.com/@ThePizzaAssembly', 'youtube_qr')
    
    # Half letter size (5.5 x 8.5 inches) - good for a card
    page_width = 5.5 * inch
    page_height = 8.5 * inch
    
    c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
    
    # Background
    c.setFillColor(CREAM)
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    
    y = page_height - 40
    
    # Logo
    logo_size = 70
    circular_logo = create_circular_logo(logo_path, logo_size * 2)
    c.drawImage(circular_logo, (page_width - logo_size) / 2, y - logo_size, 
                width=logo_size, height=logo_size, mask='auto')
    y -= logo_size + 12
    
    # Title
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_width / 2, y, "How to Make Your Pizza")
    y -= 20
    
    draw_italian_divider(c, y, page_width)
    y -= 25
    
    # Instructions
    margin = 25
    step_num = 1
    
    def draw_step(c, y, title, desc):
        nonlocal step_num
        c.setFillColor(ITALIAN_GREEN)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(margin, y, str(step_num))
        
        c.setFillColor(DARK_TEXT)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 22, y, title)
        
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 9)
        
        # Word wrap description
        words = desc.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if c.stringWidth(' '.join(current_line), "Helvetica", 9) > page_width - margin * 2 - 22:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        line_y = y - 14
        for line in lines:
            c.drawString(margin + 22, line_y, line)
            line_y -= 12
        
        step_num += 1
        return line_y - 8
    
    y = draw_step(c, y, "Rest the Dough", 
        "Remove dough from fridge and let it rest at room temperature for 1-2 hours. This makes it easier to stretch.")
    
    y = draw_step(c, y, "Stretch the Dough",
        "On a surface with semolina, push from the center outward with your fingertips, leaving the outer edge for the crust. Don't use a rolling pin!")
    
    y = draw_step(c, y, "Transfer & Top",
        "Transfer stretched dough to a pizza peel or pan with semolina. Add your toppings — the semolina prevents sticking so no need to rush.")
    
    y = draw_step(c, y, "Bake It",
        "Pizza oven: 700-900°F for 60-90 seconds. Home oven: Preheat to 450°F, bottom rack. Bake 10 minutes until crust is golden and cheese bubbles.")
    
    y -= 5
    draw_italian_divider(c, y, page_width)
    y -= 20
    
    # Pro tip
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(page_width / 2, y, "Pro Tip")
    y -= 12
    c.setFillColor(GRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(page_width / 2, y, "Preheat your pan or stone for a crispier bottom!")
    y -= 25
    
    draw_italian_divider(c, y, page_width)
    y -= 25
    
    # QR codes section
    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(page_width / 2, y, "Follow Along")
    y -= 15
    
    qr_size = 60
    qr_gap = 40
    total_width = qr_size * 2 + qr_gap
    start_x = (page_width - total_width) / 2
    
    # Instagram QR
    c.drawImage(instagram_qr, start_x, y - qr_size, width=qr_size, height=qr_size)
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(start_x + qr_size / 2, y - qr_size - 12, "Instagram")
    
    # YouTube QR
    c.drawImage(youtube_qr, start_x + qr_size + qr_gap, y - qr_size, width=qr_size, height=qr_size)
    c.drawCentredString(start_x + qr_size + qr_gap + qr_size / 2, y - qr_size - 12, "YouTube")
    
    y -= qr_size + 30
    
    # Footer
    c.setFillColor(ITALIAN_RED)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(page_width / 2, y, "@thepizzaassembly")
    
    c.save()
    print(f"Instruction card created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_instruction_card()
