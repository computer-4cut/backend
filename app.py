import os
from app import create_app

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