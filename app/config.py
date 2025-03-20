import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Config:
    """애플리케이션 설정 클래스"""

    # 기본 경로 설정
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
    QR_FOLDER = os.path.join(STATIC_FOLDER, 'qrcodes')

    # 서버 설정
    SERVER_DOMAIN = os.getenv('SERVER_DOMAIN', 'http://localhost:5000')

    # 파일 업로드 설정
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 최대 16MB 파일 업로드 제한
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # 보안 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    # 디버그 모드
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'