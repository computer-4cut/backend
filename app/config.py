import os

class Config:
    """기본 설정 클래스"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 최대 16MB 업로드 제한
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}


class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True


class TestingConfig(Config):
    """테스트 환경 설정"""
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_uploads')


class ProductionConfig(Config):
    """운영 환경 설정"""
    DEBUG = False
    # 실제 운영환경에서는 보안을 위해 SECRET_KEY를 환경 변수로 설정해야 합니다


# 환경별 설정 매핑 딕셔너리
config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}