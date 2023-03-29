from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db
from flask_paginate import Pagination, get_page_args


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home/")
def home():
    posts = Post.query.order_by(Post.id.desc())

    post = Post.query.order_by(Post.date_created.desc())

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = post.paginate(page=page, per_page=3)

    return render_template("home.html", user=current_user, posts=posts, pages=pages)


@views.route("/createpost", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        if not title:
            flash('Title cannot be empty', category='error')
        elif not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(title=title, text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_post.html", user=current_user)


@views.route("/deletepost/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    return redirect(url_for('views.home'))


@views.route("/user/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No user with that username", category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(
        author=user.id).order_by(Post.date_created.desc())

    post = Post.query.order_by(Post.date_created.desc())

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = post.paginate(page=page, per_page=3)

    return render_template("posts.html", user=current_user, posts=posts, pages=pages, username=username)


@views.route("/editpost/<id>", methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    else:
        if request.method == 'POST':
            text = request.form.get('text')

            if not text:
                flash('Post cannot be empty', category='error')
            else:
                db.session.delete(post)
                db.session.commit()

                post = Post(text=text, author=current_user.id)
                db.session.add(post)
                db.session.commit()
                flash('Post created', category='success')
                return redirect(url_for('views.home'))

    return render_template("edit_post.html", user=current_user, post=post)


@views.route('post/<slug>')
@login_required
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()

    return render_template("post_detail.html", post=post, user=current_user)
