from flask import Flask, request, jsonify

from sift_query import QueryImage, LabelNotFoundException
from utils import parse_args, _parse_args
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
        "result": None
    }
    try:
        if request.method == "POST":
            if logo is None or label is None:
                response["status_code"] = 400,
                response["message"] = "Input images is wrong format"

            logo = [query_image.convert2gray(lg) for lg in logo]
            check = query_image.add_logo2json(logo, label)

            response["status_code"] = 200
            response["message"] = "success"
            response["result"] = {}
            if check:
                response["result"]["add_logo"] = True
            else:
                response["result"]["add_logo"] = False
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
        "result": None
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
            response["result"] = {}
            if result:
                response["result"]["has_logo"] = True
            else:
                response["result"]["has_logo"] = False
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
    img, label = parse_args()
    img1, img2 = None, None
    response = {
        "status_code": None,
        "message": None,
        "result": None
    }
    if len(img) == 2:
        try:
            img1, img2 = query_image.convert2gray(img[0]), query_image.convert2gray(img[1])
        except Exception as e:
            logger.error(e)
            response["status_code"] = 400,
            response["message"] = "Input images is wrong format"
            return jsonify(response)
    try:
        if request.method == "POST":
            if img1 is None or img2 is None:
                response["status_code"] = 400,
                response["message"] = "Input images is wrong format"
                return jsonify(response)
            result = query_image.check_two_img(img1, img2, label)
            response["status_code"] = 200
            response["message"] = "success"
            response["result"] = {}
            if result:
                response["result"]["same"] = True
            else:
                response["result"]["same"] = False

    except LabelNotFoundException as e:
        logger.error(e)
        response["status_code"] = 400
        response["message"] = "Label not found in data"
    except Exception as e:
        logger.exception(e)
        response["status_code"] = 500
        response["message"] = "Internal server error"
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
