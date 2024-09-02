import os
import hashlib
from flask import Flask, Blueprint, jsonify, render_template, request, abort
from settings import UPLOADED_FILES, MAX_SiZE
from http import HTTPStatus

from helpers import not_allowed_file_ext, get_file_hash


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADED_FILES
app.config['MAX_CONTENT_LENGTH'] = MAX_SiZE

route_prefix = Blueprint('route_prefix', __name__, url_prefix='/api/v1/files')


@route_prefix.route('/')
def show_upload_page():
    return render_template('upload_form.html')


@route_prefix.route('/list', methods=['GET'])
def get_files():
    try:
        files = os.listdir(UPLOADED_FILES)
    except FileNotFoundError:
        return jsonify({'error': 'directory not found'})
    return jsonify(files)


@route_prefix.route('/<ext>', methods=['GET'])
def get_files_with_specified_extension(ext):
    files = [f for f in os.listdir(UPLOADED_FILES) if f.endswith(ext)]
    if not files:
        return jsonify({'error': 'files not found'})
    return jsonify(files)


@route_prefix.route('/create', methods=['POST'])
def create_file():
    if request.method == 'POST':
        up_files = request.files.getlist('file')
        if not up_files or all(file.filename == '' for file in up_files):
            return abort(HTTPStatus.BAD_REQUEST, description='no file selected')
        for file in up_files:
            if file and not_allowed_file_ext(file.filename):
                file_hash = hashlib.md5(file.read()).hexdigest()
                file.seek(0)
                if file_hash not in get_file_hash(UPLOADED_FILES):
                    filename = file.filename
                    up_path = os.path.join(UPLOADED_FILES, filename)
                    file.save(up_path)
            else:
                return abort(HTTPStatus.BAD_REQUEST, description='invalid file type')
        return render_template('success.html')


@route_prefix.route('/<file_name>', methods=['DELETE'])
def delete_file(file_name):
    file_path = os.path.join(UPLOADED_FILES, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"file '{file_name}' deleted successfully"})
    else:
        return jsonify({"error": f"file '{file_name}' not found"}), HTTPStatus.NOT_FOUND


@route_prefix.route('/<ext>/<file_name>', methods=['GET'])
def get_file(ext, file_name):
    file = [f for f in os.listdir(UPLOADED_FILES) if f.startswith(file_name) and f.endswith(ext)]
    return jsonify(file)


app.register_blueprint(route_prefix)


if __name__ == '__main__':
    from main import *
