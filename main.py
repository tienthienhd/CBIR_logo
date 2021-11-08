from flask import Flask, request, jsonify

from sift_query import QueryImage
from utils import parse_args

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
url_query = None
url_img_results = []

app = Flask(__name__)



@app.route("/add-logo", methods=["GET", "POST"])
def add_logo2json():
    image, filename = parse_args()
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
            return jsonify_str(response)

        try:
            query_image = QueryImage()
            logo = query_image.convert2gray(logo)
            query_image.add_logo2json(logo)
            check = True
        except Exception as e:
            response["status_code"] = 500
            response["message"] = "Internal server error"
            raise response from e

        response["status_code"] = 200
        response["message"] = "success"
        if check:
            response["result"]["add_logo"] = True
            return jsonify_str(response)
        else:
            response["result"]["add_logo"] = False
            return jsonify_str(response)


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
                return jsonify_str(response)

            query_image = QueryImage()
            img = query_image.convert2gray(img[0])
            result = query_image.check_img_have_logo(img)
            response["status_code"] = 200
            response["message"] = "success"
            if result:
                response["result"]["has_logo"] = True
                return jsonify_str(response)
            else:
                response["result"]["has_logo"] = False
                return jsonify_str(response)
    except Exception as e:
        response["status_code"] = 500
        response["message"] = "Internal server error"
        raise response from e

@app.route("/compare", methods=["GET", "POST"])
def compare():
    query_image = QueryImage()
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
        except:
            response["status_code"] = 400,
            response["message"] = "Input images is wrong format"
            return jsonify_str(response)

    if request.method == "POST":
        if img1 is None or img2 is None:
            response["status_code"] = 400,
            response["message"] = "Input images is wrong format"
            return jsonify_str(response)
        result = query_image.check_two_img(img1, img2)
        response["status_code"] = 200
        response["message"] = "success"
        if result:
            response["result"]["same"] = True
            return jsonify_str(response)
        else:
            response["result"]["same"] = False
            return jsonify_str(response)


def jsonify_str(output_list):
    with app.app_context():
        with app.test_request_context():
            result = jsonify(output_list)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
