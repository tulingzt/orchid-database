from flask import Blueprint, render_template

# 网页页面路由
html = Blueprint('html', __name__)

@html.route("/")
def index():
    return render_template('index.html')