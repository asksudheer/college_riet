from flask import render_template
from flask_login import current_user
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='College Management System')

@bp.route('/about')
def about():
    return render_template('about.html', title='About Us')

@bp.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')
