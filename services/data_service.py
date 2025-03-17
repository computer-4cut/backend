UPLOAD_FOLDER = 'uploads'
QR_FOLDER = 'qrcodes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class DataService:
    def allowed_file(filename):
        """허용된 파일 확장자인지 확인"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def generate_unique_filename(original_filename):
        """고유한 파일명 생성"""
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{timestamp}_{unique_id}.{ext}"


    def generate_qr_code(url, qr_path):
        """QR 코드 생성"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_path)
        return qr_path