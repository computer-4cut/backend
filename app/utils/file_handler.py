import os
import uuid
from flask import current_app, url_for
from werkzeug.utils import secure_filename


def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file):
    secure_name = secure_filename(file.filename)
    ext = os.path.splitext(secure_name)[1].lower()
    unique_filename = f"{str(uuid.uuid4())}{ext}"

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

    try:
        file.save(file_path)
    except Exception as e:
        raise ValueError(f"파일 저장 중 오류 발생: {str(e)}")

    return unique_filename, file_path


def get_file_url(filename, request):
    return request.host_url.rstrip('/') + url_for('api_bp.get_uploaded_file', filename=filename)


def cleanup_old_files(days=1):
    import time

    count = 0
    now = time.time()
    upload_folder = current_app.config['UPLOAD_FOLDER']

    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)

        file_mod_time = os.path.getmtime(file_path)

        # 설정된 기간보다 오래된 파일 삭제
        if now - file_mod_time > days * 86400: # 86400초 = 1일
            try:
                os.remove(file_path)
                count += 1
            except:
                pass

    return count