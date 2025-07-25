"""
Simple script to create a basic icon for Lexia
You can replace this with a proper .ico file later
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_lexia_icon():
    # Create a 256x256 image with a blue background
    size = 256
    img = Image.new('RGBA', (size, size), (52, 152, 219, 255))  # Blue background
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle
    circle_margin = 40
    draw.ellipse([circle_margin, circle_margin, size-circle_margin, size-circle_margin], 
                 fill=(255, 255, 255, 255))
    
    # Try to draw text (fallback if font not available)
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Draw "L" in the center
    text = "L"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10
    
    draw.text((x, y), text, fill=(52, 152, 219, 255), font=font)
    
    # Save as ICO (multiple sizes)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
    images = []
    
    for icon_size in icon_sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Save as .ico file
    images[0].save('lexia.ico', format='ICO', sizes=[(img.width, img.height) for img in images])
    print("Icon created: lexia.ico")

if __name__ == "__main__":
    try:
        create_lexia_icon()
    except ImportError:
        print("PIL (Pillow) not available. Creating placeholder icon...")
        # Create a simple placeholder
        with open('lexia.ico', 'wb') as f:
            # This is a minimal 16x16 ICO file structure (placeholder)
            ico_header = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x20\x00\x68\x04\x00\x00\x16\x00\x00\x00'
            f.write(ico_header)
            # Add minimal bitmap data (blue square)
            bitmap_data = b'\x00' * 1128  # Minimal bitmap data
            f.write(bitmap_data)
        print("Placeholder icon created: lexia.ico")