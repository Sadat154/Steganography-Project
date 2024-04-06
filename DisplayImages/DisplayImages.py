from pathlib import Path

def create_html_for_images(folder_path, num_images):
    # Create the HTML file
    html_filename = "StegImgResults.html"
    with open(html_filename, "w") as html_file:
        # Write the HTML header
        html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Image Gallery</title>\n</head>\n<body>\n")

        # Get a list of image files in the specified folder
        image_files = [filename for filename in Path(folder_path).iterdir() if filename.suffix.lower() in (".jpg", ".png", ".gif")]

        # Limit the number of images to the specified count
        num_images = min(num_images, len(image_files))

        # Write image tags to the HTML file
        for i in range(num_images):
            image_path = image_files[i]
            html_file.write(f'<img src="{image_path}" alt="Image {i+1}">\n')

        # Write the HTML footer
        html_file.write("</body>\n</html>")

    print(f"HTML file '{html_filename}' created successfully!")

# Example usage:
folder_with_images = "path/to/your/image/folder"
num_images_to_display = 5
create_html_for_images(folder_with_images, num_images_to_display)
