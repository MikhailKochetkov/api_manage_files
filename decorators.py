import os

from flask import jsonify


up = os.getenv('UPLOADED_FILES', default='./uploads')


def check_dir_readable(func):
    def readable_wrapper(*args, **kwargs):
        if os.access(up, os.R_OK):
            return func(*args, **kwargs)
        else:
            return jsonify(
                {'error': 'read access to directory denied'}
            )
    readable_wrapper.__name__ = func.__name__
    return readable_wrapper


def check_dir_executable(func):
    def execuatble_wrapper(*args, **kwargs):
        if os.access(up, os.X_OK):
            return func(*args, **kwargs)
        else:
            return jsonify(
                {'error': 'execuate access to directory denied'}
            )
    execuatble_wrapper.__name__ = func.__name__
    return execuatble_wrapper


def check_dir_writable(func):
    def writable_wrapper():
        if os.access(up, os.W_OK):
            return func()
        else:
            return jsonify(
                {'error': 'write access to directory denied'}
            )
    writable_wrapper.__name__ = func.__name__
    return writable_wrapper
