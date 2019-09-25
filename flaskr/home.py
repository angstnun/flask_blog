import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required

homeBlueprint = Blueprint('home', __name__, url_prefix='/home')

@homeBlueprint.route('/', methods=('GET', 'POST'))
@login_required
def index():
    return render_template("home/index.html")