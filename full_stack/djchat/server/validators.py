import os

from django.core.exceptions import ValidationError
from PIL import Image


# Validator function to check the dimensions of an image
def validate_icon_image_size(image):
    # Check if an image is provided
    if image:
        # Open the image using PIL
        with Image.open(image) as img:
            # Check if the image dimensions exceed the allowed size
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The maximum allowed dimensions for the image are 70x70 - size of image you uploaded: {img.size}"
                )

# Validator function to check the file extension of an image
def validate_image_file_extension(value):
    # Extract the file extension from the file name
    ext = os.path.splitext(value.name)[1]
    # List of valid file extensions
    valid_extensions = ['.jpeg', '.jpg', '.png', '.gif']
    # Check if the file extension is not in the list of valid extensions
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension")
