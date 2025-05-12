import qrcode
from io import BytesIO
from PIL import Image
import base64


def create_url_qr(url, box_size=10, border=4, error_correction=None):
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

    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_buffered = BytesIO()
    qr_img.save(qr_buffered, format="PNG")
    qr_buffered.seek(0)

    return qr_buffered


def create_image_data_qr(image_data, resize=True, max_size=(400, 400), quality=70):
    if isinstance(image_data, str):
        image = Image.open(image_data)
    else:
        image = Image.open(image_data)

    if resize:
        image.thumbnail(max_size)

    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=quality)
    img_str = base64.b64encode(buffered.getvalue()).decode()

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(img_str)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_buffered = BytesIO()
    qr_img.save(qr_buffered, format="PNG")
    qr_buffered.seek(0)

    return qr_buffered