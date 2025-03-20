from flask import request, jsonify, send_from_directory
from app import app, data_service
from app.config import Config
import os


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    이미지 업로드 API 엔드포인트

    클라이언트에서 전송된 이미지를 처리하고 QR 코드를 생성합니다.
    """
    # 요청에 파일이 포함되어 있는지 확인
    if 'image' not in request.files:
        return jsonify({'error': '이미지 파일이 없습니다'}), 400

    file = request.files['image']

    # 데이터 서비스를 통해 이미지 처리
    result = data_service.process_image_upload(file)

    if result is None:
        return jsonify({'error': '이미지 처리 중 오류가 발생했습니다'}), 400

    return jsonify(result), 200


@app.route('/images/<filename>')
def get_image(filename):
    """
    이미지 조회 엔드포인트

    Args:
        filename (str): 이미지 파일명
    """
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


@app.route('/qrcodes/<filename>')
def get_qrcode(filename):
    """
    QR 코드 조회 엔드포인트

    Args:
        filename (str): QR 코드 파일명
    """
    return send_from_directory(Config.QR_FOLDER, filename)


@app.route('/share/<filename>')
def share_page(filename):
    """
    이미지 공유 페이지 엔드포인트

    Args:
        filename (str): 이미지 파일명
    """
    # 파일 존재 여부 확인
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return "이미지를 찾을 수 없습니다", 404

    # HTML 템플릿 생성
    html = data_service.get_html_share_template(filename)

    return html


@app.route('/health')
def health_check():
    """
    서버 상태 확인 엔드포인트
    """
    return jsonify({'status': 'ok'}), 200


@app.errorhandler(404)
def not_found(error):
    """
    404 에러 핸들러
    """
    return jsonify({'error': '요청한 리소스를 찾을 수 없습니다'}), 404


@app.errorhandler(413)
def too_large(error):
    """
    413 에러 핸들러 (파일 크기 초과)
    """
    return jsonify({'error': '파일 크기가 너무 큽니다. 최대 16MB까지 업로드 가능합니다'}), 413


@app.errorhandler(500)
def server_error(error):
    """
    500 에러 핸들러
    """
    app.logger.error(f'서버 오류: {error}')
    return jsonify({'error': '서버 내부 오류가 발생했습니다'}), 500