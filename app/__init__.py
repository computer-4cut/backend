from flask import Flask
from app.config import Config
from service.data_service import DataService
import os

# Flask 앱 인스턴스 생성
app = Flask(__name__, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)

# DataService 인스턴스 생성
data_service = DataService(
    upload_folder=Config.UPLOAD_FOLDER,
    qr_folder=Config.QR_FOLDER,
    server_domain=Config.SERVER_DOMAIN,
    allowed_extensions=Config.ALLOWED_EXTENSIONS
)

# 정적 파일 디렉토리 생성
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.QR_FOLDER, exist_ok=True)

# 라우트 임포트 (순환 참조 방지를 위해 여기서 임포트)
from app import routes