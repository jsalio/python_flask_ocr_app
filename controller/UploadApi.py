import io
import os
from flask import Blueprint, render_template, request, send_file
from werkzeug.utils import secure_filename
from ocr_service import images_to_searchable_pdf

upload_api = Blueprint('upload_api', __name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_api.route("/upload", methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        files = request.files.getlist('files')
        valid = [f for f in files if f and f.filename and allowed_file(f.filename)]
        if not valid:
            return render_template('upload.html', msg='No valid image files selected (PNG, JPG, JPEG)')

        lang = request.form.get('lang', 'eng')
        pdf_bytes = images_to_searchable_pdf(valid, lang=lang)

        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='searchable.pdf'
        )

    return render_template('upload.html')
