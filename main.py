import os

from endpoints import app


up = os.getenv('UPLOADED_FILES', default='./uploads')

if not os.path.exists(up):
    os.mkdir(up)

if __name__ == '__main__':
    app.run(debug=True)
