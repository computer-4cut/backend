import os
import uuid
from flask import current_app, url_for
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """업로드된 파일이 허용된 확장자를 가지는지 확인

    Args:
        filename: 확인할 파일 이름

    Returns:
        bool: 허용된 확장자이면 True, 아니면 False
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file):
    """업로드된 파일을 저장하고 파일 경로 반환

    Args:
        file: 업로드된 파일 객체

    Returns:
        tuple: (파일명, 파일 경로, 접근 가능한 URL)

    Raises:
        ValueError: 파일 저장 과정에서 오류 발생 시
    """
    # 파일명 보안 처리 및 중복 방지를 위한 UUID 추가
    secure_name = secure_filename(file.filename)
    ext = os.path.splitext(secure_name)[1].lower()
    unique_filename = f"{str(uuid.uuid4())}{ext}"

    # 파일 저장 경로
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

    try:
        file.save(file_path)
    except Exception as e:
        raise ValueError(f"파일 저장 중 오류 발생: {str(e)}")

    return unique_filename, file_path


def get_file_url(filename, request):
    """저장된 파일의 접근 가능한 URL 생성

    Args:
        filename: 파일명
        request: Flask 요청 객체

    Returns:
        str: 파일 접근 URL
    """
    return request.host_url.rstrip('/') + url_for('api_bp.get_uploaded_file', filename=filename)


def cleanup_old_files(days=1):
    """일정 기간이 지난 업로드 파일 정리

    Args:
        days: 보관 기간 (일)

    Returns:
        int: 삭제된 파일 수
    """
    import time

    count = 0
    now = time.time()
    upload_folder = current_app.config['UPLOAD_FOLDER']

    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)

        # 파일 수정 시간 확인
        file_mod_time = os.path.getmtime(file_path)

        # 설정된 기간보다 오래된 파일 삭제
        if now - file_mod_time > days * 86400:  # days * 24 * 60 * 60
            try:
                os.remove(file_path)
                count += 1
            except:
                pass

    return count