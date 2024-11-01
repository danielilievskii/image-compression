from flask import Flask, request, render_template, send_file
import os
import cv2
from utils import (rle_compress_and_save, load_and_rle_decompress, jpeg_compress)

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
COMPRESSED_FOLDER = 'static/compressed/'
DECOMPRESSED_FOLDER = 'static/decompressed/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(COMPRESSED_FOLDER):
    os.makedirs(COMPRESSED_FOLDER)

if not os.path.exists(DECOMPRESSED_FOLDER):
    os.makedirs(DECOMPRESSED_FOLDER)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rle-compress', methods=['POST'])
def rle_compress_image():
    if 'image' not in request.files:
        return "No image part"

    file = request.files['image']
    if file.filename == '':
        return "No selected file"

    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        image = cv2.imread(filename, 0)
        compressed_file_path = os.path.join(COMPRESSED_FOLDER, file.filename + '_compressed_data.txt')
        rle_compress_and_save(image, compressed_file_path)
        return send_file(compressed_file_path, as_attachment=True)


@app.route('/rle-decompress', methods=['POST'])
def rle_decompress_file():
    if 'text_file' not in request.files:
        return "No text file part"

    file = request.files['text_file']
    if file.filename == '':
        return "No selected file"

    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        decompressed_image = load_and_rle_decompress(filename)
        if decompressed_image is None:
            return "Error decompressing file"
        decompressed_image_path = os.path.join(DECOMPRESSED_FOLDER, 'decompressed_image.bmp')
        cv2.imwrite(decompressed_image_path, decompressed_image)
        return send_file(decompressed_image_path, as_attachment=True)


@app.route('/jpeg-compress', methods=['POST'])
def jpeg_compress_image():
    if 'image' not in request.files or 'jpeg_quality' not in request.form:
        return "No image or JPEG quality part"

    file = request.files['image']
    jpeg_quality = int(request.form['jpeg_quality'])

    if file.filename == '':
        return "No selected file"

    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        compressed_file_path = os.path.join(COMPRESSED_FOLDER, 'compressed_' + file.filename)
        try:
            jpeg_compress(filename, compressed_file_path, jpeg_quality)
            return send_file(compressed_file_path, as_attachment=True)
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    app.run(debug=True)