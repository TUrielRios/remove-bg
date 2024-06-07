import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from rembg import remove
from PIL import Image

app = Flask(__name__, static_folder="static")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

#Creamos las rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == "":
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        output_filename = 'no_bg_' + os.path.splitext(file.filename)[0] + '.png'
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        process_image(file_path, output_path)
        return redirect(url_for('show_images', original=file.filename, processed = output_filename))

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'],filename)

@app.route('/show_images')
def show_images():
    original = request.args.get('original')
    processed = request.args.get('processed')
    return render_template('show_images.html', original=original, processed=processed)
    

def process_image(input_path,output_path):
    with open(input_path, 'rb') as i:
        img= Image.open(i)
        img = remove(img)
        img.save(output_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
