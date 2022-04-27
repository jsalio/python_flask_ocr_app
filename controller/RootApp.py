from flask import Blueprint, render_template

app_api = Blueprint('app_api', __name__)

@app_api.route("/app")
def home_page():
        return render_template('index.html') 