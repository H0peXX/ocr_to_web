from flask import Flask, request, jsonify, render_template_string
import os
from werkzeug.utils import secure_filename
from ocr.typhoon_ocr.ocr_utils import ocr_document
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# HTML template for the upload form
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OCR Document Upload</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .upload-form { border: 2px dashed #ccc; padding: 20px; text-align: center; }
        .result { margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>OCR Document Upload</h1>
        <div class="upload-form">
            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf,.png,.jpg,.jpeg" required>
                <button type="submit">Upload and Process</button>
            </form>
        </div>
        <div id="result" class="result"></div>
    </div>
    <script>
        document.getElementById('uploadForm').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const resultDiv = document.getElementById('result');
            resultDiv.textContent = 'Processing...';
            
            try {
                const response = await fetch('/api/ocr', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (response.ok) {
                    resultDiv.textContent = data.result;
                } else {
                    resultDiv.textContent = 'Error: ' + data.error;
                }
            } catch (error) {
                resultDiv.textContent = 'Error: ' + error.message;
            }
        };
    </script>
</body>
</html>
"""

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Supported file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/ocr', methods=['POST'])
def ocr_api():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    try:
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Supported types are: PNG, JPG, JPEG, PDF'}), 400
            
        # Perform OCR
        result = ocr_document(
            pdf_or_image_path=filepath,
            task_type="default",
            target_image_dim=1800,
            target_text_length=8000,
            page_num=1
        )
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
