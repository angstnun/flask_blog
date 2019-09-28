from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort   

from flaskr.auth import login_required
from . import db

blogBlueprint = Blueprint('blog', __name__)


@blogBlueprint.route('/')
def index():
    dbSession = db.GetSession()
    posts = dbSession.query(db.Post).filter_by(isActive=True).all()
    return render_template('blog/index.html', posts=posts)


@blogBlueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    try:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            error = None

            if not title:
                error = 'Title is required.'

            if error is not None:
                flash(error)
            else:
                dbSession = db.GetSession()
                newPost = db.Post(
                    author_id=g.user.id,
                    title=title,
                    text=body
                )
                dbSession.add(newPost)
                dbSession.commit()
                return redirect(url_for('blog.index'))

        return render_template('blog/create.html')
    except Exception as blogBlueprintException:
        error = f"Oh no, something went wrong: {str(blogBlueprintException)}"
        flash(error)
        return render_template('/error.html')

def get_post(id, check_author=True):
    dbSession = db.GetSession()
    post = dbSession.query(db.Post, db.User).\
        filter(db.Post.author_id == db.User.id).\
        filter(db.Post.id == id).scalar()

    if post is None:
        abort(404, f"Post doesn't exist: {id}")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

@blogBlueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            dbSession = db.GetSession()
            post = dbSession.query(db.Post).\
                filter_by(id=id).\
                scalar()
            post.title = title
            post.text = body
            dbSession.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@blogBlueprint.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    dbSession = db.GetSession()
    post = dbSession.query(db.Post).\
        filter_by(id=id).\
        scalar()
    post.isActive = 0
    dbSession.commit()
    return redirect(url_for('blog.index'))
