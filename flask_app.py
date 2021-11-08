import cv2.cv2
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from sift_feature.sift_query import Query_Image
from utils import parse_args
from sift_feature.query import query_img, match_and_box


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
url_query = None
url_img_results = []

app = Flask(__name__)


@app.route("/addlogo2json", methods=["GET", "POST"])
def add_logo2json():
    image, filename = parse_args()
    logo = image[0]
    if request.method == "POST":
        if logo is None:
            return jsonify_str({"error", "Please upload logo as input"})
        Q = Query_Image()
        check = False
        try:
            logo = Q.convert2gray(logo)
            Q.add_logo2json(logo)
            check = True
        except Exception as e:
            raise "Process add logo error!!!"
        if check:
            return jsonify_str({"Result": "You added a logo success to file json"})


@app.route("/checklogo", methods=["GET", "POST"])
def check_logo():
    img, filenames = parse_args()
    try:
        if request.method == "POST":
            if img is None:
                return jsonify_str({"error": "Please upload photos as input"})
            Q = Query_Image()
            img = Q.convert2gray(img[0])
            result = Q.check_img_have_logo(img)
            if result:
                return jsonify_str({"result": "Image have pepsi logo"})
            else:
                return jsonify_str({"result": "Image not have pepsi logo"})
    except Exception as e:
        print(e)


@app.route("/compare", methods=["GET", "POST"])
def compare():
    Q = Query_Image()
    img, filenames = parse_args()
    img1, img2 = None, None
    if len(img) == 2:
        img1, img2 = Q.convert2gray(img[0]), Q.convert2gray(img[1])

    if request.method == "POST":
        if img1 is None or img2 is None:
            return jsonify_str({"error": "Please chooses or upload two photos as input"})
        result = Q.check_two_img(img1, img2)
        if result:
            return jsonify_str({"results": "Both pictures are of the SAME logo of PEPSI"})
        else:
            return jsonify_str({"results": "Both images are DIFFERENT logo"})


# @app.route('/match')
# def match():
#     img_path = request.args['img_path']
#     img_path = 'static/' + img_path
#
#     if os.path.exists('static/imgs/matched_kp.png'):
#         os.remove('static/imgs/matched_kp.png')
#     if os.path.exists('static/imgs/matched_kp_filtered.png'):
#         os.remove('static/imgs/matched_kp_filtered.png')
#
#     match_and_box(img_path_1=url_query, img_path_2=img_path)
#
#     return render_template('results.html', non_filter='imgs/matched_kp.png', filtered='imgs/matched_kp_filted.png')
#
# from flask import make_response
# from functools import wraps, update_wrapper
# from datetime import datetime
#
# def nocache(view):
#     @wraps(view)
#     def no_cache(*args, **kwargs):
#         response = make_response(view(*args, **kwargs))
#         response.headers['Last-Modified'] = datetime.now()
#         response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#         response.headers['Pragma'] = 'no-cache'
#         response.headers['Expires'] = '-1'
#         return response
#
#     return update_wrapper(no_cache, view)


@app.route('/show_result/<img>')
def show_result(img):
    # preprocess

    return render_template('result_single.html')


def jsonify_str(output_list):
    with app.app_context():
        with app.test_request_context():
            result = jsonify(output_list)
    return result


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            # return redirect(request.url)
            return jsonify_str({'error': 'Cannot get image'})
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return jsonify_str({'error': 'Cannot get image'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            url_local = os.path.join('static/imgs', filename)
            file.save(url_local)
            global url_query
            url_query = url_local
            return 'Ok'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug='development')
