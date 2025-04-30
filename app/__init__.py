from flask import Flask
import os
from app.config import config_by_name


def create_app(config_name='dev'):
    """애플리케이션 팩토리 함수

    각종 설정과 확장 프로그램을 초기화하고 애플리케이션 인스턴스를 반환합니다.

    Args:
        config_name: 설정 이름 ('dev', 'test', 'prod' 중 하나)

    Returns:
        Flask 애플리케이션 인스턴스
    """
    app = Flask(__name__)

    # 설정 불러오기
    app.config.from_object(config_by_name[config_name])

    # 업로드 폴더 생성
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # API 블루프린트 등록
    from app.api.routes import api_bp
    app.register_blueprint(api_bp)

    return app