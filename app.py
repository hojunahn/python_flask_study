from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
from werkzeug.utils import secure_filename
from routes.ex import process_excel

# 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'routes'))

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/data', methods=['GET'])
def get_data():
    # 업로드된 파일이 있는지 확인
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not uploaded_files:
        return jsonify({'error': 'No file uploaded'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_files[0])

    try:
        category_totals = process_excel(file_path)
        return jsonify({'category_totals': category_totals})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        category_totals = process_excel(file_path)
        return jsonify({'category_totals': category_totals})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
