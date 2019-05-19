from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
url_query = None
url_img_results = []

app = Flask(__name__)

from sift_feature.query import query_img, match_and_box
import json
with open("sift_feature/dict_logo.json") as json_file:
    data = json.load(json_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == "POST":
        if url_query is None:
            return jsonify_str({'error': 'Please upload or add link image.'})
        results = query_img(url_query, data)
        print('Finished query----------------')
        print(results)
        return jsonify_str({"results": results})


@app.route('/match')
def match():
    img_path = request.args['img_path']
    img_path = 'static/' + img_path

    if os.path.exists('static/imgs/matched_kp.png'):
        os.remove('static/imgs/matched_kp.png')
    if os.path.exists('static/imgs/matched_kp_filtered.png'):
        os.remove('static/imgs/matched_kp_filtered.png')


    match_and_box(img_path_1=url_query, img_path_2=img_path)

    return render_template('results.html', non_filter='imgs/matched_kp.png', filtered='imgs/matched_kp_filted.png')


# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r


from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response


    return update_wrapper(no_cache, view)

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