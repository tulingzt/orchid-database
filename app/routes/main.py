from flask import Blueprint, render_template
from app import db

# 网页页面路由
html = Blueprint('html', __name__)

@html.route("/login.html")
def login_html():
    return render_template('login.html')

@html.route("/dashboard.html")
def dashboard_html():
    return render_template('dashboard.html')

@html.route("/")
def index():
    return render_template('register.html')