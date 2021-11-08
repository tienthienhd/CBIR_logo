import werkzeug
from flask import Flask, request, jsonify
from flask_restful import reqparse

from sift_query import QueryImage
from utils import parse_args, parse_request
from loguru import logger

logger.add('logs/merch_client.log', rotation="50 MB", retention='1 week')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
url_query = None
url_img_results = []

app = Flask(__name__)
query_image = QueryImage()


@app.route("/add-logo", methods=["GET", "POST"])
def add_logo2json():
    image, filename = parse_args()

    parser = reqparse.RequestParser()
    parser.add_argument('image', required=True, location=['form', 'args', 'files', 'json'], action='append')
    parser.add_argument('label', required=True, location=['form', 'args', 'files', 'json'])
    args_ = parser.parse_args(strict=True)
    if len(args_['image']) > 0 and "FileStorage" in args_['image'][0]:
        parser.replace_argument('image', type=werkzeug.datastructures.FileStorage, required=True, location='files',
                                action='append')
    args_ = parser.parse_args(strict=True)

    images = args_['image']
    imgs, filenames = parse_request(images)
    label = args_['label']

    logo = image[0]
    response = {
        "status_code": None,
        "message": None,
        "result": {}
    }
    if request.method == "POST":

        if logo is None:
            response["status_code"] = 400,
            response["message"] = "Input images is wrong format"
            return jsonify(response)

        try:
            logo = query_image.convert2gray(logo)
            check = query_image.add_logo2json(logo)
        except Exception as e:
            logger.error(e)
            response["status_code"] = 500
            response["message"] = "Internal server error"
            return response

        response["status_code"] = 200
        response["message"] = "success"
        if check:
            response["result"]["add_logo"] = True

        else:
            response["result"]["add_logo"] = False
        return jsonify(response)


@app.route("/check-logo", methods=["GET", "POST"])
def check_logo():
    img, filenames = parse_args()
    response = {
        "status_code": None,
        "message": None,
        "result": {}
    }
    try:
        if request.method == "POST":
            if img is None:
                response["status_code"] = 400,
                response["message"] = "Input images is wrong format"
                return jsonify(response)

            img = query_image.convert2gray(img[0])
            result = query_image.check_img_have_logo(img)
            response["status_code"] = 200
            response["message"] = "success"
            if result:
                response["result"]["has_logo"] = True
                return jsonify(response)
            else:
                response["result"]["has_logo"] = False
                return jsonify(response)
    except Exception as e:
        logger.error(e)
        response["status_code"] = 500
        response["message"] = "Internal server error"
        raise response from e


@app.route("/compare", methods=["GET", "POST"])
def compare():
    img, filenames = parse_args()
    img1, img2 = None, None
    response = {
        "status_code": None,
        "message": None,
        "result": {}
    }
    if len(img) == 2:
        try:
            img1, img2 = query_image.convert2gray(img[0]), query_image.convert2gray(img[1])
        except Exception as e:
            logger.error(e)
            response["status_code"] = 400,
            response["message"] = "Input images is wrong format"
            return jsonify(response)

    if request.method == "POST":
        if img1 is None or img2 is None:
            response["status_code"] = 400,
            response["message"] = "Input images is wrong format"
            return jsonify(response)
        result = query_image.check_two_img(img1, img2)
        response["status_code"] = 200
        response["message"] = "success"
        if result:
            response["result"]["same"] = True
            return jsonify(response)
        else:
            response["result"]["same"] = False
            return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
