try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from werkzeug.utils import secure_filename
from crypt import methods
import time
import os
from tokenize import String
from controller.RootApp import app_api 

import redis
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.register_blueprint(app_api)

cache = redis.Redis(host='redis', port=6379)

# define a folder to store and later serve the images
UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

# @app.route('/app')
# def home_page():
#         return render_template('index.html')           

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        #this a text remove for for return code to normally
        for var in list(range(1000)) :
            # check if there is a file in the request
            if 'file' not in request.files:
                return render_template('upload.html', msg='No file selected')
            file = request.files['file']
            # if no file is selected
            if file.filename == '':
                return render_template('upload.html', msg='No file selected')

            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                # call the OCR function on it
                extracted_text = ocr_core(file)
                print("Loop {} :", var)

                # extract the text and display it
                return render_template('upload.html',
                                       msg='Successfully processed',
                                       extracted_text=extracted_text,
                                       img_src=UPLOAD_FOLDER + filename)
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times. Welcome to python Loser x \n'.format(count)