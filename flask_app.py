from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
url_query = None
url_img_results = []

app = Flask(__name__)

from utils.query import query_img
import json
with open("./utils/dict_logo.json") as json_file:
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
        return jsonify_str({"results": results})


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



app.run(host='0.0.0.0', port=5000, debug='development')