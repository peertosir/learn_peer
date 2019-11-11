from learn_peer_app import app
from flask import render_template, Blueprint

core = Blueprint('core', __name__)


@core.route('/')
def index():
    #TO-DO
    return render_template('index.html')