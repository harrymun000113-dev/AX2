import os
from PIL import Image, ImageDraw, ImageFont
from data import TRAVEL_DATA

def generate_placeholder_images():
    if not os.path.exists('assets'):
        os.makedirs('assets')

    for country, info in TRAVEL_DATA.items():
        # Create a new image with the primary color
        width, height = 800, 400
        image = Image.new('RGB', (width, height), color=info['color'])
        draw = ImageDraw.Draw(image)

        # Draw a simple pattern or secondary color element
        draw.rectangle([width//4, height//4, width*3//4, height*3//4], fill=info['secondary_color'])
        
        # Add text
        try:
            # Try to use a common system font, or fallback to default
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        text = f"{country} ({info['name_en']})"
        # Calculate text position using box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Draw shadow
        draw.text((position[0]+2, position[1]+2), text, font=font, fill=(0, 0, 0))
        # Draw main text
        draw.text(position, text, font=font, fill=(255, 255, 255) if info['secondary_color'] != (255, 255, 255) else (0,0,0))

        # Save the image
        image.save(info['image_path'])
        print(f"Generated image for {country} at {info['image_path']}")

if __name__ == "__main__":
    generate_placeholder_images()
