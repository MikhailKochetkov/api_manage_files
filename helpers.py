import os
import hashlib

from settings import ALLOWED_EXTENSIONS


def get_file_hash(folder_path):
    files_hash = []
    for name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, name)
        if os.path.isfile(file_path):
            hash_md5 = hashlib.md5()
            with open(file_path, 'rb') as n:
                for chunk in iter(lambda: n.read(4096), b''):
                    hash_md5.update(chunk)
            files_hash.append(hash_md5.hexdigest())
    return files_hash


def not_allowed_file_ext(filename):
    return os.path.splitext(filename)[1][1:] not in ALLOWED_EXTENSIONS
