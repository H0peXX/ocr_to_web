from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
# สมมติว่ามีฟังก์ชัน ocr_image ใน ocr/typhoon_ocr/ocr_utils.py
from ocr.typhoon_ocr.ocr_utils import ocr_image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        # เรียกใช้ฟังก์ชัน OCR (แก้ไขชื่อฟังก์ชันตามที่มีจริง)
        result = ocr_image(filepath)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)
