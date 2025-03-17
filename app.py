from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
data_service = DataService()

# 업로드된 이미지와 QR 코드가 저장될 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
QR_FOLDER = 'qrcodes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 디렉토리가 없다면 생성
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['QR_FOLDER'] = QR_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB 파일 업로드 제한

@app.route('/')
def health_check():
    try:
        return jsonify({'state': 'healthy'}), 200
    except Exception as e:
        return jsonify({'state': 'unhealthy', 'error': str(e)}), 500





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)