from PIL import Image
import os

def create_lsb_images_html(images_folder, output_html_path):
    html_content = "<html><head><title>LSB Images</title></head><body>"

    for filename in os.listdir(images_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(images_folder, filename)
            lsb_image_path = os.path.join(images_folder, f"lsb_{filename}")

            # Create LSB image
            create_lsb_image(image_path, lsb_image_path)

            # Add image to HTML content
            html_content += f"<h3>{filename}</h3>"
            html_content += f"<img src='{filename}' alt='Original Image' style='margin-right: 10px;'>"
            html_content += f"<img src='lsb_{filename}' alt='LSB Image'><br><br>"

    html_content += "</body></html>"

    with open(output_html_path, "w") as html_file:
        html_file.write(html_content)

def create_lsb_image(input_image_path, output_image_path):
    original_image = Image.open(input_image_path)
    lsb_image = original_image.convert("1")  # Convert to 1-bit image (black and white)
    lsb_image.save(output_image_path)

# Example usage
images_folder = 'path/to/your/images'
output_html_path = 'lsb_images.html'

create_lsb_images_html(images_folder, output_html_path)
