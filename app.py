from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
from rembg import remove
from PIL import Image


app = Flask(__name__, static_folder='static')  # Configuración de la carpeta estática
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

# Crea los directorios si no existen
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        output_filename = 'no_bg_' + os.path.splitext(file.filename)[0] + '.png'
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        process_image(file_path, output_path)
        return redirect(url_for('show_images', original=file.filename, processed=output_filename))

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/show_images')
def show_images():
    original = request.args.get('original')
    processed = request.args.get('processed')
    return render_template('show_images.html', original=original, processed=processed)

def process_image(input_path, output_path):
    with open(input_path, 'rb') as i:
        img = Image.open(i)
        img = remove(img)
        img.save(output_path)

if __name__ == '__main__':
    app.run(debug=True)