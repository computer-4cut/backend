import os
import uuid
import qrcode
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image


class DataService:
    """데이터 처리 서비스 클래스"""

    def __init__(self, upload_folder, qr_folder, server_domain, allowed_extensions=None):
        """
        서비스 초기화

        Args:
            upload_folder (str): 이미지 업로드 경로
            qr_folder (str): QR 코드 저장 경로
            server_domain (str): 서버 도메인
            allowed_extensions (set): 허용된 파일 확장자
        """
        self.upload_folder = upload_folder
        self.qr_folder = qr_folder
        self.server_domain = server_domain
        self.allowed_extensions = allowed_extensions or {'png', 'jpg', 'jpeg'}

        # 디렉토리가 없으면 생성
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.qr_folder, exist_ok=True)

    def is_allowed_file(self, filename):
        """
        허용된 파일 확장자인지 확인

        Args:
            filename (str): 파일명

        Returns:
            bool: 허용된 확장자면 True, 아니면 False
        """
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def generate_unique_filename(self, original_filename):
        """
        고유한 파일명 생성

        Args:
            original_filename (str): 원본 파일명

        Returns:
            str: 고유한 파일명
        """
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{timestamp}_{unique_id}.{ext}"

    def save_uploaded_file(self, file_storage):
        """
        업로드된 파일 저장

        Args:
            file_storage (FileStorage): 업로드된 파일 객체

        Returns:
            tuple: (파일명, 파일 경로) 또는 오류시 (None, None)
        """
        if not file_storage or file_storage.filename == '':
            return None, None

        if not self.is_allowed_file(file_storage.filename):
            return None, None

        filename = secure_filename(file_storage.filename)
        unique_filename = self.generate_unique_filename(filename)
        file_path = os.path.join(self.upload_folder, unique_filename)

        try:
            file_storage.save(file_path)

            # 이미지 검증
            try:
                img = Image.open(file_path)
                img.verify()  # 올바른 이미지인지 확인
            except Exception as e:
                # 이미지가 올바르지 않으면 삭제하고 None 반환
                os.remove(file_path)
                return None, None

            return unique_filename, file_path
        except Exception as e:
            # 파일 저장 실패 시 None 반환
            return None, None

    def generate_qr_code(self, data, filename=None):
        """
        QR 코드 생성

        Args:
            data (str): QR 코드에 포함될 데이터 (URL 등)
            filename (str, optional): 저장할 파일명. 기본값은 None으로 자동 생성.

        Returns:
            tuple: (QR 코드 파일명, 파일 경로)
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4())
            filename = f"qr_{timestamp}_{unique_id}.png"

        qr_path = os.path.join(self.qr_folder, filename)

        # QR 코드 생성
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_path)

        return filename, qr_path

    def get_image_url(self, filename):
        """
        이미지 URL 생성

        Args:
            filename (str): 파일명

        Returns:
            str: 이미지 URL
        """
        return f"{self.server_domain}/images/{filename}"

    def get_qr_url(self, filename):
        """
        QR 코드 URL 생성

        Args:
            filename (str): 파일명

        Returns:
            str: QR 코드 URL
        """
        return f"{self.server_domain}/qrcodes/{filename}"

    def get_share_url(self, filename):
        """
        공유 URL 생성

        Args:
            filename (str): 파일명

        Returns:
            str: 공유 URL
        """
        return f"{self.server_domain}/share/{filename}"

    def process_image_upload(self, file_storage):
        """
        이미지 업로드 처리 메인 함수

        Args:
            file_storage (FileStorage): 업로드된 파일 객체

        Returns:
            dict: 처리 결과 데이터 또는 None
        """
        # 파일 저장
        unique_filename, file_path = self.save_uploaded_file(file_storage)
        if not unique_filename:
            return None

        # URL 생성
        image_url = self.get_image_url(unique_filename)
        share_url = self.get_share_url(unique_filename)

        # QR 코드 생성
        qr_filename = f"qr_{unique_filename}"
        self.generate_qr_code(share_url, qr_filename)
        qr_url = self.get_qr_url(qr_filename)

        # 결과 데이터
        result = {
            'filename': unique_filename,
            'image_url': image_url,
            'qr_url': qr_url,
            'share_url': share_url
        }

        return result

    def get_html_share_template(self, filename):
        """
        이미지 공유 페이지 HTML 템플릿 생성

        Args:
            filename (str): 이미지 파일명

        Returns:
            str: HTML 템플릿
        """
        image_url = self.get_image_url(filename)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>공유된 이미지</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }}
                img {{ max-width: 100%; max-height: 80vh; margin: 20px auto; display: block; }}
                h1 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>공유된 이미지</h1>
            <img src="{image_url}" alt="공유된 이미지">
            <p>이 이미지는 QR 코드를 통해 공유되었습니다.</p>
        </body>
        </html>
        """