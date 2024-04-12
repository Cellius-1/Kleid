from flask import Flask, request, send_file, jsonify
from PIL import Image
from io import BytesIO
from utils import validate_image_file, validate_secret_text

app = Flask(__name__)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kleid -Steganography </title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <h1>Kleidl</h1>
    <label for="original-image">Select an image:</label>
    <input type="file" id="original-image" accept="image/*">
    <label for="secret-text">Enter secret text:</label>
    <textarea id="secret-text" rows="4"></textarea>
    <button id="hide-button">Hide Text</button>
  </div>

  <script src="script.js"></script>
</body>
</html>'''

@app.route('/hide', methods=['POST'])
def hide_text():
    original_image = request.files['image']
    secret_text = request.form['secret_text']

    # Validate image and secret text
    try:
        validate_image_file(original_image.filename)
        validate_secret_text(secret_text)

        img = Image.open(original_image)
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

        output_buffer = BytesIO()
        img.save(output_buffer, format='PNG')
        output_buffer.seek(0)

        return send_file(output_buffer, attachment_filename='hidden_image.png', as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
