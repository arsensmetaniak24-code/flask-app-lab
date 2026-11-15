from flask import render_template, redirect, url_for, flash, request, session

from app import db
from . import posts_bp
from .models import Post
from .forms import PostForm, DeleteForm


@posts_bp.route("")
def all_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active)
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("all_posts.html", title="Posts", posts=posts)


@posts_bp.route("/<int:post_id>")
def detail_post(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template("detail_post.html", title=post.title, post=post)


@posts_bp.route("/create", methods=["GET", "POST"])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            author=session.get("username", "Anonymous"),
        )
        db.session.add(post)
        db.session.commit()
        flash(f"Post \"{post.title}\" added successfully", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))

    if request.method == "POST":
        flash("Enter the correct data in the form", "danger")

    return render_template("add_post.html", title="New Post", form=form)


@posts_bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)

    if request.method == "GET":
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))

    if request.method == "POST":
        flash("Enter the correct data in the form", "danger")

    return render_template("add_post.html", title="Edit Post", form=form, post=post)


@posts_bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = DeleteForm()

    if form.validate_on_submit():
        title = post.title
        db.session.delete(post)
        db.session.commit()
        flash(f"Post \"{title}\" deleted", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template("delete_confirm.html", title="Delete Post", post=post, form=form)
