from flask import render_template, Blueprint

main = Blueprint("main",__name__)

@main.route('/')
def index():
    return "Hello World!"