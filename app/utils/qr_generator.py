import qrcode
from io import BytesIO
from PIL import Image
import base64


def create_url_qr(url, box_size=10, border=4, error_correction=None):
    """URL을 QR 코드로 변환

    Args:
        url: QR 코드에 인코딩할 URL
        box_size: QR 코드의 각 상자 크기 (픽셀)
        border: QR 코드 주변의 여백 크기
        error_correction: 오류 수정 수준 (None=기본값, L, M, Q, H)

    Returns:
        BytesIO: QR 코드 이미지가 포함된 BytesIO 객체
    """
    # 오류 수정 수준 설정
    if error_correction is None:
        error_correction = qrcode.constants.ERROR_CORRECT_L
    elif error_correction == 'L':
        error_correction = qrcode.constants.ERROR_CORRECT_L
    elif error_correction == 'M':
        error_correction = qrcode.constants.ERROR_CORRECT_M
    elif error_correction == 'Q':
        error_correction = qrcode.constants.ERROR_CORRECT_Q
    elif error_correction == 'H':
        error_correction = qrcode.constants.ERROR_CORRECT_H

    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # QR 코드 이미지 생성
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # BytesIO에 저장
    qr_buffered = BytesIO()
    qr_img.save(qr_buffered, format="PNG")
    qr_buffered.seek(0)

    return qr_buffered


def create_image_data_qr(image_data, resize=True, max_size=(400, 400), quality=70):
    """이미지 데이터를 직접 QR 코드로 변환

    인코딩된 이미지 데이터를 직접 QR 코드에 포함시킵니다.
    이미지 크기가 크면 QR 코드가 복잡해져 인식률이 떨어질 수 있습니다.

    Args:
        image_data: 이미지 파일 객체나 경로
        resize: 이미지 크기 조정 여부
        max_size: 최대 이미지 크기 (가로, 세로)
        quality: JPEG 압축 품질 (1-100)

    Returns:
        BytesIO: QR 코드 이미지가 포함된 BytesIO 객체
    """
    # 이미지 열기
    if isinstance(image_data, str):
        # 파일 경로인 경우
        image = Image.open(image_data)
    else:
        # 파일 객체인 경우
        image = Image.open(image_data)

    # 이미지 크기 조정 (선택 사항)
    if resize:
        image.thumbnail(max_size)

    # 이미지를 base64 문자열로 변환
    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=quality)
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # base64 이미지 데이터로 QR 코드 생성
    qr = qrcode.QRCode(
        version=None,  # 자동으로 크기 설정
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 높은 오류 수정 수준
        box_size=10,
        border=1,
    )
    qr.add_data(img_str)
    qr.make(fit=True)

    # QR 코드 이미지 생성
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # BytesIO에 저장
    qr_buffered = BytesIO()
    qr_img.save(qr_buffered, format="PNG")
    qr_buffered.seek(0)

    return qr_buffered