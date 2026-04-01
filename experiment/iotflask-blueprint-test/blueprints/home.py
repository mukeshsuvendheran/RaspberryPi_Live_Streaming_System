# blueprints/home.py
from flask import Blueprint, render_template

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    return "Welcome to the home page!"
