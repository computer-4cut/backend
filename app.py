import os
from app.config import config_by_name
from flask import Flask

# 애플리케이션 생성 함수 정의
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

# 환경 변수에서 설정 이름을 가져오거나 기본값으로 'dev' 사용
config_name = os.getenv('FLASK_CONFIG', 'dev')

# 애플리케이션 생성
app = create_app(config_name)

if __name__ == '__main__':
    # 호스트 및 포트 설정 (환경 변수 또는 기본값)
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'

    # 애플리케이션 실행
    app.run(host=host, port=port, debug=debug)