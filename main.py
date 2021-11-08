from flask import Flask, request, jsonify

from sift_query import QueryImage
from utils import parse_args

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
url_query = None
url_img_results = []

app = Flask(__name__)


response_example = {
    'status_code': 200, 500, 400,
    'message': 'Internal Server error',
    'result': {
    'has_logo': True,
    ''
}
}


@app.route("/add-logo", methods=["GET", "POST"])
def add_logo2json():
    image, filename = parse_args()
    logo = image[0]
    if request.method == "POST":
        if logo is None:
            return jsonify_str({"error", "Please upload logo as input"})
        query_image = QueryImage()
        check = False
        try:
            logo = query_image.convert2gray(logo)
            query_image.add_logo2json(logo)
            check = True
        except Exception as e:
            raise Exception("Process add logo error!!!") from e
        if check:
            return jsonify_str({"result": "You added a logo success to file json"})


@app.route("/check-logo", methods=["GET", "POST"])
def check_logo():
    img, filenames = parse_args()
    try:
        if request.method == "POST":
            if img is None:
                return jsonify_str({"error": "Please upload photos as input"})
            query_image = QueryImage()
            img = query_image.convert2gray(img[0])
            result = query_image.check_img_have_logo(img)
            if result:
                return jsonify_str({"result": "Image have pepsi logo"})
            else:
                return jsonify_str({"result": "Image not have pepsi logo"})
    except Exception as e:
        print(e)


@app.route("/compare", methods=["GET", "POST"])
def compare():
    query_image = QueryImage()
    img, filenames = parse_args()
    img1, img2 = None, None
    if len(img) == 2:
        img1, img2 = query_image.convert2gray(img[0]), Q.convert2gray(img[1])

    if request.method == "POST":
        if img1 is None or img2 is None:
            return jsonify_str({"error": "Please chooses or upload two photos as input"})
        result = query_image.check_two_img(img1, img2)
        if result:
            return jsonify_str({"results": "Both pictures are of the SAME logo of PEPSI"})
        else:
            return jsonify_str({"results": "Both images are DIFFERENT logo"})


def jsonify_str(output_list):
    with app.app_context():
        with app.test_request_context():
            result = jsonify(output_list)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
