from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', items=['banana', 'apple', 'orange'])

@views.route('/<name>')
def name(name):
    return render_template('name.html', name=name)

# @views.route('/')