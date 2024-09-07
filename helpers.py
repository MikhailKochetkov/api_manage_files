import os
import hashlib

from settings import NOT_ALLOWED_EXTENSIONS


def get_uploaded_file_hash(folder_path: str) -> list[str]:
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


def not_allowed_file_ext(filename: str) -> bool:
    return (os.path.splitext(filename.lower())[1][1:]
            not in NOT_ALLOWED_EXTENSIONS)
