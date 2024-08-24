import hashlib
import os

from settings import ALLOWED_EXTENSIONS


def get_file_hash(file):
    pass


def allowed_file(filename):
    return os.path.splitext(filename)[1][1:] in ALLOWED_EXTENSIONS

