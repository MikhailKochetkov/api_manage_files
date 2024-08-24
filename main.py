import os

from endpoints import app
from settings import UPLOADED_FILES


if not os.path.exists(UPLOADED_FILES):
    os.mkdir(UPLOADED_FILES)

if __name__ == '__main__':
    app.run(debug=True)
