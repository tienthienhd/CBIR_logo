from flask import Flask, request, jsonify

from sift_query import QueryImage, LabelNotFoundException
from utils import parse_args, _parse_args, lb_parse_args
from loguru import logger

logger.add('logs/CBIR_logo.log', rotation="50 MB", retention='1 week')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
url_query = None
url_img_results = []

app = Flask(__name__)
query_image = QueryImage()


@app.route("/add-logo", methods=["GET", "POST"])
def add_logo2json():
    logo, label = _parse_args()
    response = {
        "status_code": None,
        "message": None,
        "add_logo": None
    }
    try:
        if request.method == "POST":
            if logo is None or label is None:
                response["status_code"] = 400,
                response["message"] = "Input images is wrong format"
                return jsonify(response)

            logo = [query_image.convert2gray(lg) for lg in logo]
            check = query_image.add_logo2json(logo, label)
            response["status_code"] = 200
            response["message"] = "success"
            if check:
                response["add_logo"] = True
            else:
                response["add_logo"] = False
    except Exception as e:
        logger.exception(e)
        response["status_code"] = 500
        response["message"] = "Internal server error"

    return jsonify(response)


@app.route("/check-logo", methods=["GET", "POST"])
def check_logo():
    img, label = _parse_args()
    response = {
        "status_code": None,
        "message": None,
        "has_logo": None
    }
    try:
        if request.method == "POST":
            if img is None or img[0] is None:
                response["status_code"] = 400
                response["message"] = "Input images is wrong format"
                return jsonify(response)

            img = query_image.convert2gray(img[0])
            result = query_image.check_img_have_logo(img, label)
            response["status_code"] = 200
            response["message"] = "success"
            if result:
                response["has_logo"] = True
            else:
                response["has_logo"] = False
    except LabelNotFoundException as e:
        logger.error(e)
        response["status_code"] = 400
        response["message"] = "Label not found in data"
    except Exception as e:
        logger.exception(e)
        response["status_code"] = 500
        response["message"] = "Internal server error"
    return jsonify(response)


@app.route("/compare", methods=["GET", "POST"])
def compare():
    img = parse_args()
    img1, img2 = None, None
    response = {
        "status_code": None,
        "message": None,
        "same": None,
        "label": None
    }
    if len(img) == 2:
        img1, img2 = query_image.convert2gray(img[0]), query_image.convert2gray(img[1])
    try:
        if request.method == "POST":
            if img1 is None or img2 is None:
                response["status_code"] = 400,
                response["message"] = "Input images is wrong format"
                return jsonify(response)

            result, label = query_image.check_two_img(img1, img2)
            response["status_code"] = 200
            response["message"] = "success"
            response["label"] = label
            if result:
                response["same"] = True
            else:
                response["same"] = False

    except LabelNotFoundException as e:
        logger.error(e)
        response["status_code"] = 400
        response["message"] = "Label not found in data"
    except Exception as e:
        logger.exception(e)
        response["status_code"] = 500
        response["message"] = "Internal server error"
    return jsonify(response)

@app.route("/delete_logo", methods=["GET", "POST"])
def delete_logo():
    label = lb_parse_args()
    response = {
        "status_code": None,
        "message": None,
        "deleted": None
    }
    try:
        if request.method == "POST":
            result = query_image.delete_logo(label)
            response["status_code"] = 200
            response["message"] = "success"
            response["deleted"] = result
            return response
    except Exception as e:
        logger.exception(e)
        response["status_code"] = 500
        response["message"] = "Internal server error"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
