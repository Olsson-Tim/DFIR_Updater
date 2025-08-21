from PIL import Image, ImageDraw

# Create a new image with a blue background and a white checkmark
image = Image.new('RGBA', (256, 256), (45, 45, 45, 255))  # Dark gray background
draw = ImageDraw.Draw(image)

# Draw a blue circle
draw.ellipse((28, 28, 228, 228), fill=(58, 126, 191, 255))  # Blue circle

# Draw a white checkmark
draw.line((80, 128, 110, 158), fill=(255, 255, 255, 255), width=16)
draw.line((110, 158, 176, 96), fill=(255, 255, 255, 255), width=16)

# Save as ICO
image.save('assets/icon.ico', format='ICO')
print("Icon created successfully!")