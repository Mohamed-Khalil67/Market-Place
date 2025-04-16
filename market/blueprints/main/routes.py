# market/blueprints/main/routes.py
from flask import render_template, redirect, url_for
from flask_login import login_required
from market.blueprints.main import main_bp

@main_bp.route('/')
@main_bp.route('/home')
def home_page():
    return render_template('main/home.html')

@main_bp.route('/about')
def about_page():
    return render_template('main/about.html')
