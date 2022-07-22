from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)

from flaskBlog import db
from flaskBlog.models import Post
from flask_login import current_user, login_required

from flaskBlog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        created_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(created_post)
        db.session.commit()
        flash('Your post has been created !', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    single_post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=single_post.title, post=single_post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    updated_post = Post.query.get_or_404(post_id)
    if updated_post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        updated_post.title = form.title.data
        updated_post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated !', 'success')
        return redirect(url_for('posts.post', post_id=updated_post.id))

    if request.method == 'GET':
        form.title.data = updated_post.title
        form.content.data = updated_post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    deleted_post = Post.query.get_or_404(post_id)
    if deleted_post.author != current_user:
        abort(403)
    db.session.delete(deleted_post)
    db.session.commit()
    flash('Your post has been deleted !', 'success')
    return redirect(url_for('main.home'))
