import os
from app import create_app

config_name = os.getenv('FLASK_CONFIG', 'dev')

app = create_app(config_name)

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'

    app.run(host=host, port=port, debug=debug)