from PIL import Image
from utils import validate_image_file, validate_secret_text

def hide_text_in_image(image_path, secret_text):
    img = Image.open(image_path)
    binary_secret_text = ''.join(format(ord(char), '08b') for char in secret_text)
    secret_text_length = len(binary_secret_text)
    img_data = iter(img.getdata())

    new_img_data = []
    for i in range(secret_text_length):
        pixel = next(img_data)
        new_pixel = list(pixel)
        new_pixel[-1] = int(binary_secret_text[i])
        new_img_data.append(tuple(new_pixel))

    img.putdata(new_img_data)
    img.save('hidden_image.png')

def reveal_text_in_image(hidden_image_path):
    img = Image.open(hidden_image_path)
    img_data = iter(img.getdata())

    binary_secret_text = ''
    while True:
        pixel = next(img_data)
        binary_secret_text += str(pixel[-1])
        if len(binary_secret_text) % 8 == 0:
            secret_text = ''.join(chr(int(binary_secret_text[i:i+8], 2)) for i in range(0, len(binary_secret_text), 8))
            return secret_text

if __name__ == "__main__":
    original_image_path = input("Enter the path of the original image file: ")
    validate_image_file(original_image_path)

    secret_text = input("Enter the text to hide: ")
    validate_secret_text(secret_text)

    hide_text_in_image(original_image_path, secret_text)
    print("Text hidden successfully in the image.")

    hidden_image_path = 'hidden_image.png'
    print("The hidden image file is saved as:", hidden_image_path)
