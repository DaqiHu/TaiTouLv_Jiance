from PIL import Image

def compress_to_360p(input_image_path, output_image_path):
    # Open the image file
    with Image.open(input_image_path) as img:
        # Calculate new width based on 360p height
        aspect_ratio = img.width / img.height
        new_width = int(360 * aspect_ratio)

        # Resize the image
        img = img.resize((new_width, 360), Image.LANCZOS)

        # Save the compressed image
        img.save(output_image_path, optimize=True)

input_image_path = r"\\wsl.localhost\Ubuntu\home\dantalion\GitHub\yolov7\temp\source\camera.jpg"
output_image_path = r"\\wsl.localhost\Ubuntu\home\dantalion\GitHub\yolov7\temp\source\camera_edited.jpg"

compress_to_360p(input_image_path, output_image_path)
