from flask import Blueprint, request, send_file, jsonify, current_app, send_from_directory
import os
from app.utils.file_handler import allowed_file, save_uploaded_file, get_file_url
from app.utils.qr_generator import create_url_qr, create_image_data_qr

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'
    })


@api_bp.route('/api/v1/qr/url', methods=['POST'])
def convert_image_to_url_qr():
    if 'image' not in request.files:
        return jsonify({'error': '이미지가 업로드되지 않았습니다'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': '이미지가 선택되지 않았습니다'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': '지원되지 않는 파일 형식입니다'}), 400

    try:
        filename, file_path = save_uploaded_file(file)

        image_url = get_file_url(filename, request)

        box_size = int(request.form.get('box_size', 10))
        border = int(request.form.get('border', 4))
        error_correction = request.form.get('error_correction', 'L')

        qr_img_buffer = create_url_qr(
            image_url,
            box_size=box_size,
            border=border,
            error_correction=error_correction
        )

        return send_file(qr_img_buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/api/v1/qr/data', methods=['POST'])
def convert_image_to_data_qr():
    if 'image' not in request.files:
        return jsonify({'error': '이미지가 업로드되지 않았습니다'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': '이미지가 선택되지 않았습니다'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': '지원되지 않는 파일 형식입니다'}), 400

    try:
        resize = request.form.get('resize', 'true').lower() == 'true'
        max_width = int(request.form.get('max_width', 400))
        max_height = int(request.form.get('max_height', 400))
        quality = int(request.form.get('quality', 70))

        qr_img_buffer = create_image_data_qr(
            file,
            resize=resize,
            max_size=(max_width, max_height),
            quality=quality
        )

        return send_file(qr_img_buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500