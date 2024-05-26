from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
app.secret_key = 'supersecretkey'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Dummy function to simulate text model
def process_text_model(input_text):
    return f"Processed text: {input_text}"

# Dummy function to simulate image model
def process_image_model(image_path):
    return f"Processed image saved to: {image_path}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'textinput' in request.form:
            input_text = request.form['textinput']
            text_result = process_text_model(input_text)
            return render_template('index.html', text_result=text_result)

        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_result = process_image_model(filepath)
                return render_template('index.html', image_result=image_result)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

