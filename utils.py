import base64
import io
import re
import ssl
import cv2
import numpy as np
import requests
import werkzeug
from PIL import Image
from urllib3 import poolmanager

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=ctx)


class ImageException(Exception):
    pass


def url_to_image(url):
    """Download image from url"""
    # session = requests.session()
    # session.mount('https://', TLSAdapter())
    res = requests.get(url, timeout=5, verify=False)
    # session.close()
    image = np.asarray(bytearray(res.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def is_support_type(filename):
    """Check type support"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def stream_to_image(stream):
    """Parser image in bytes"""
    npimg = np.fromstring(stream.read(), np.int8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return img


def string_to_image(img_string):
    """Parser image from base64"""
    img_string = re.sub('^data:image/[a-z]+;base64,', '', img_string)
    imgdata = base64.b64decode(img_string)

    image = Image.open(io.BytesIO(imgdata))
    img = np.array(image)

    if img.ndim == 3 and img.shape[2] > 3:
        img = img[:, :, :3]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def parse_request(images):
    imgs = []
    filenames = []
    try:
        for image in images:
            img = None
            filename = None
            if isinstance(image, str):
                if len(image) < 2:
                    raise ImageException("String image is wrong format")
                if image.startswith("http"):
                    img = url_to_image(image)
                    filename = "url"
                else:
                    img = string_to_image(image)
                    filename = "base64"
            elif isinstance(image, werkzeug.datastructures.FileStorage):
                if is_support_type(image.filename):
                    img = stream_to_image(image)
                    filename = image.filename
            imgs.append(img)
            filenames.append(filename)
    except:
        raise ImageException("Image is not exist or wrong format")
    return imgs, filenames


