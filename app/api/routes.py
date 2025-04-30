from flask import Blueprint, request, send_file, jsonify, current_app, send_from_directory
import os
from app.utils.file_handler import allowed_file, save_uploaded_file, get_file_url
from app.utils.qr_generator import create_url_qr, create_image_data_qr

# API 블루프린트 생성
api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/uploads/<filename>')
def get_uploaded_file(filename):
    """업로드된 파일 제공

    Args:
        filename: 요청된 파일 이름

    Returns:
        파일 응답
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """서버 상태 확인 엔드포인트

    Returns:
        JSON: 서버 상태 정보
    """
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'
    })


@api_bp.route('/api/v1/qr/url', methods=['POST'])
def convert_image_to_url_qr():
    """이미지를 업로드하여 URL 기반 QR 코드로 변환

    업로드된 이미지를 서버에 저장하고 해당 이미지의 URL을 QR 코드로 생성합니다.

    Returns:
        QR 코드 이미지 또는 에러 메시지
    """
    # 이미지 업로드 확인
    if 'image' not in request.files:
        return jsonify({'error': '이미지가 업로드되지 않았습니다'}), 400

    file = request.files['image']

    # 파일 선택 확인
    if file.filename == '':
        return jsonify({'error': '이미지가 선택되지 않았습니다'}), 400

    # 허용된 파일 형식 확인
    if not allowed_file(file.filename):
        return jsonify({'error': '지원되지 않는 파일 형식입니다'}), 400

    try:
        # 파일 저장
        filename, file_path = save_uploaded_file(file)

        # 이미지 URL 생성
        image_url = get_file_url(filename, request)

        # QR 코드 설정
        box_size = int(request.form.get('box_size', 10))
        border = int(request.form.get('border', 4))
        error_correction = request.form.get('error_correction', 'L')

        # URL을 QR 코드로 변환
        qr_img_buffer = create_url_qr(
            image_url,
            box_size=box_size,
            border=border,
            error_correction=error_correction
        )

        # QR 코드 이미지 반환
        return send_file(qr_img_buffer, mimetype='image/png')

    except Exception as e:
        # 오류 처리
        return jsonify({'error': str(e)}), 500


@api_bp.route('/api/v1/qr/data', methods=['POST'])
def convert_image_to_data_qr():
    """이미지를 업로드하여 이미지 데이터 기반 QR 코드로 변환

    업로드된 이미지 데이터를 직접 QR 코드에 인코딩합니다.
    이미지 크기가 크면 QR 코드가 복잡해져 인식률이 떨어질 수 있습니다.

    Returns:
        QR 코드 이미지 또는 에러 메시지
    """
    # 이미지 업로드 확인
    if 'image' not in request.files:
        return jsonify({'error': '이미지가 업로드되지 않았습니다'}), 400

    file = request.files['image']

    # 파일 선택 확인
    if file.filename == '':
        return jsonify({'error': '이미지가 선택되지 않았습니다'}), 400

    # 허용된 파일 형식 확인
    if not allowed_file(file.filename):
        return jsonify({'error': '지원되지 않는 파일 형식입니다'}), 400

    try:
        # 이미지 크기 설정
        resize = request.form.get('resize', 'true').lower() == 'true'
        max_width = int(request.form.get('max_width', 400))
        max_height = int(request.form.get('max_height', 400))
        quality = int(request.form.get('quality', 70))

        # 이미지 데이터를 직접 QR 코드로 변환
        qr_img_buffer = create_image_data_qr(
            file,
            resize=resize,
            max_size=(max_width, max_height),
            quality=quality
        )

        # QR 코드 이미지 반환
        return send_file(qr_img_buffer, mimetype='image/png')

    except Exception as e:
        # 오류 처리
        return jsonify({'error': str(e)}), 500