from flask import Flask, request, jsonify
import werkzeug
from flask_restful import reqparse
from sift_query import QueryImage, LabelNotFoundException
from utils import ImageException, parse_request
from loguru import logger

logger.add('logs/CBIR_logo.log', rotation="50 MB", retention='1 week')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
url_query = None
url_img_results = []

app = Flask(__name__)
query_image = QueryImage(rate=.6, nOctaveLayers=6)


@app.route("/add-logo", methods=["GET", "POST"])
def add_logo2json():
    response = {
        "status_code": None,
        "message": None,
        "add_logo": None,
        "label": None,
        "quantity_add": None
    }
    try:
        parser = reqparse.RequestParser()
        parser.add_argument("image", required=True, location=["form", "args", "files", "json"], action="append")
        parser.add_argument("label", required=False, location=["form", "args", "files", "json"])
        args_ = parser.parse_args()
        if len(args_['image']) > 0 and "FileStorage" in args_['image'][0]:
            parser.replace_argument('image', type=werkzeug.datastructures.FileStorage, required=True, location='files',
                                    action='append')
        args_ = parser.parse_args()
        images = args_['image']
        label = args_["label"]

        logo, filename = parse_request(images)

        if request.method == "POST":
            for lg in logo:
                if lg is None or label is None:
                    response["status_code"] = 400
                    response["message"] = "Input images is wrong format"
                    return jsonify(response)
            logo = [query_image.convert2gray(lg) for lg in logo]
            check = query_image.add_logo2json(logo, label)
            response["status_code"] = 200
            response["message"] = "success"
            response["label"] = label
            response["quantity_add"] = len(logo)
            if check:
                response["add_logo"] = True
            else:
                response["add_logo"] = False


    except ImageException as e:
        logger.error(e)
        response["status_code"] = 400
        response["message"] = "Image is not exist or wrong format"

    except Exception as e:
        logger.exception(e)
        response["status_code"] = 500
        response["message"] = "Internal server error"

    return jsonify(response)


@app.route("/check-logo", methods=["GET", "POST"])
def check_logo():
    response = {
        "status_code": None,
        "message": None,
        "has_logo": None
    }
    try:
        parser = reqparse.RequestParser()
        parser.add_argument("image", required=True, location=["form", "args", "files", "json"], action="append")
        parser.add_argument("label", required=True, location=["form", "args", "files", "json"])
        args_ = parser.parse_args()
        if len(args_['image']) > 0 and "FileStorage" in args_['image'][0]:
            parser.replace_argument('image', type=werkzeug.datastructures.FileStorage, required=True, location='files',
                                    action='append')
        args_ = parser.parse_args()
        images = args_['image']
        label = args_["label"]
        imgs, filename = parse_request(images)

        if request.method == "POST":
            if imgs[0] is None:
                response["status_code"] = 400
                response["message"] = "Input images is wrong format"
                return jsonify(response)

            image = query_image.convert2gray(imgs[0])
            result = query_image.check_img_have_logo(image, label)
            response["status_code"] = 200
            response["message"] = "success"
            if result:
                response["has_logo"] = True
            else:
                response["has_logo"] = False

    except ImageException as e:
        logger.error(e)
        response["status_code"] = 400
        response["message"] = "Image is not exist or wrong format"

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
    response = {
        "status_code": None,
        "message": None,
        "same": None,
        "label": None
    }
    try:
        parser = reqparse.RequestParser()
        parser.add_argument("image", required=True, location=["form", "args", "files", "json"], action="append")
        parser.add_argument("label", location=["form", "args", "files", "json"], action="append")
        args_ = parser.parse_args()
        if len(args_['image']) > 0 and "FileStorage" in args_['image'][0]:
            parser.replace_argument('image', type=werkzeug.datastructures.FileStorage, required=True, location='files',
                                    action='append')
        args_ = parser.parse_args()
        images = args_['image']
        lb = args_["label"]
        img, filename = parse_request(images)
        img1, img2 = None, None
        if len(img) == 2:
            img1, img2 = query_image.convert2gray(img[0]), query_image.convert2gray(img[1])
        if request.method == "POST":
            if img1 is None or img2 is None:
                response["status_code"] = 400
                response["message"] = "Input images is wrong format"
                return jsonify(response)

            result, label = query_image.check_two_img(img1, img2, lb)
            response["status_code"] = 200
            response["message"] = "success"
            response["label"] = label
            if result:
                response["same"] = True
            else:
                response["same"] = False

    except ImageException as e:
        logger.error(e)
        response["status_code"] = 400
        response["message"] = "Image is not exist or wrong format"
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
    response = {
        "status_code": None,
        "message": None,
        "deleted": None,
        "label": None
    }
    try:
        parser = reqparse.RequestParser()
        parser.add_argument("label", required=True, location=["form", "args", "files", "json"])
        args_ = parser.parse_args(strict=True)
        label = args_["label"]
        if request.method == "POST":
            result = query_image.delete_logo(label)
            response["status_code"] = 200
            response["message"] = "success"
            response["deleted"] = result
            response["label"] = label
            return response

    except ImageException as e:
        logger.error(e)
        response["status_code"] = 400
        response["message"] = "Image is not exist or wrong format"

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
