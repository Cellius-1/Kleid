import os

def validate_image_file(image_path):
    """is it a valid imag e file"""
    if not os.path.exists(image_path):
        raise FileNotFoundError("File not found, try checking the original location: {}".format(image_path))
    if not os.path.isfile(image_path):
        raise ValueError("Not a file: {}".format(image_path))
    _, ext = os.path.splitext(image_path)
    valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    if ext.lower() not in valid_extensions:
        raise ValueError("Not an image, accepted extensions are PNG, JPG, JPEG, BMP, and GIF: {}".format(ext))

def validate_secret_text(secret_text):
    """check if the text is empty"""
    if len(secret_text) == 0:
        raise ValueError("Secret text cannot be empty")
    # You can add more validation rules here if needed

def validate_hidden_image(hidden_image_path):
    """check if the given file is a valid hidden image file."""
    validate_image_file(hidden_image_path)
    if os.path.basename(hidden_image_path) != 'hidden_image.png':
        raise ValueError("Invalid hidden image filename: {}".format(hidden_image_path))
