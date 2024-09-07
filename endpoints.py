import os
import hashlib

from http import HTTPStatus
from flask import (Flask,
                   Blueprint,
                   jsonify,
                   render_template,
                   request,
                   abort)

from settings import UPLOADED_FILES, MAX_SiZE
from helpers import not_allowed_file_ext, get_file_hash
from decorators import (check_dir_readable,
                        check_dir_execuatble,
                        check_dir_writable)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADED_FILES
app.config['MAX_CONTENT_LENGTH'] = MAX_SiZE

route_prefix = Blueprint('route_prefix',
                         __name__,
                         url_prefix='/api/v1/files')


@route_prefix.route('/')
def show_upload_page():
    return render_template('upload_form.html')


@route_prefix.route('/create', methods=['POST'])
@check_dir_writable
def create_file():
    if request.method == 'POST':
        up_files = request.files.getlist('file')
        if not up_files or all(file.filename == '' for file in up_files):
            return abort(
                HTTPStatus.BAD_REQUEST,
                description='no file selected'
            )
        for file in up_files:
            if file and not_allowed_file_ext(file.filename):
                file_hash = hashlib.md5(file.read()).hexdigest()
                file.seek(0)
                if file_hash not in get_file_hash(UPLOADED_FILES):
                    up_path = os.path.join(UPLOADED_FILES, file.filename)
                    try:
                        file.save(up_path)
                    except Exception as e:
                        return abort(
                            HTTPStatus.INTERNAL_SERVER_ERROR,
                            description=f'error saving file: {str(e)}')
                else:
                    return abort(
                        HTTPStatus.BAD_REQUEST,
                        description='file already exists'
                    )
            else:
                return abort(
                    HTTPStatus.BAD_REQUEST,
                    description='invalid file type'
                )
        return render_template('success.html')


@route_prefix.route('/list', methods=['GET'])
@check_dir_readable
def get_files():
    try:
        files = os.listdir(UPLOADED_FILES)
        return jsonify(files)
    except FileNotFoundError:
        return jsonify({'error': 'no such directory'})


@route_prefix.route('/<ext>/<file_name>', methods=['GET'])
@check_dir_readable
def get_file(ext, file_name):
    try:
        file = [f for f in os.listdir(UPLOADED_FILES)
                if f.startswith(file_name) and f.endswith(ext)]
        return jsonify(file)
    except FileNotFoundError:
        return jsonify({'error': 'no such file or directory'})


@route_prefix.route('/<ext>', methods=['GET'])
@check_dir_readable
def get_files_spec_ext(ext):
    try:
        files = [f for f in os.listdir(UPLOADED_FILES) if f.endswith(ext)]
        return jsonify(files)
    except FileNotFoundError:
        return jsonify({'error': 'no such file or directory'})


@route_prefix.route('/<file_name>', methods=['DELETE'])
@check_dir_execuatble
def delete_file(file_name):
    file_path = os.path.join(UPLOADED_FILES, file_name)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return jsonify(
                {"message": f"file '{file_name}' deleted successfully"}
            ), HTTPStatus.OK
        except Exception as e:
            return jsonify(
                {"error": f"error deleting file '{file_name}': {str(e)}"}
            ), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return jsonify(
            {"error": f"file '{file_name}' not found"}
        ), HTTPStatus.NOT_FOUND


app.register_blueprint(route_prefix)

if __name__ == '__main__':
    from main import *
