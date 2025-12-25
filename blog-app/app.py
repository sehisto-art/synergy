{\rtf1\ansi\ansicpg1251\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
from flask import Flask, render_template, redirect, url_for, flash, request, abort\
from flask_login import LoginManager, login_user, logout_user, login_required, current_user\
from werkzeug.security import generate_password_hash, check_password_hash\
\
from config import Config\
from models import db, User, Post, Tag, Comment\
from forms import RegisterForm, LoginForm, PostForm, CommentForm\
\
\
def create_app():\
    app = Flask(__name__)\
    app.config.from_object(Config)\
\
    os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)\
\
    db.init_app(app)\
\
    login_manager = LoginManager(app)\
    login_manager.login_view = "login"\
\
    @login_manager.user_loader\
    def load_user(user_id):\
        return User.query.get(int(user_id))\
\
    with app.app_context():\
        db.create_all()\
\
    @app.route("/")\
    def index():\
        tag_name = request.args.get("tag")\
        if tag_name:\
            tag = Tag.query.filter_by(name=tag_name).first()\
            if tag:\
                posts = tag.posts.filter(Post.is_public == True).order_by(Post.created_at.desc())\
            else:\
                posts = []\
        else:\
            posts = Post.query.filter_by(is_public=True).order_by(Post.created_at.desc())\
        return render_template("index.html", posts=posts, tag_name=tag_name)\
\
    @app.route("/register", methods=["GET", "POST"])\
    def register():\
        if current_user.is_authenticated:\
            return redirect(url_for("index"))\
        form = RegisterForm()\
        if form.validate_on_submit():\
            if User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first():\
                flash("\uc0\u1055 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1100  \u1089  \u1090 \u1072 \u1082 \u1080 \u1084  \u1080 \u1084 \u1077 \u1085 \u1077 \u1084  \u1080 \u1083 \u1080  email \u1091 \u1078 \u1077  \u1089 \u1091 \u1097 \u1077 \u1089 \u1090 \u1074 \u1091 \u1077 \u1090 .")\
                return redirect(url_for("register"))\
            user = User(\
                username=form.username.data,\
                email=form.email.data,\
                password_hash=generate_password_hash(form.password.data),\
            )\
            db.session.add(user)\
            db.session.commit()\
            flash("\uc0\u1056 \u1077 \u1075 \u1080 \u1089 \u1090 \u1088 \u1072 \u1094 \u1080 \u1103  \u1091 \u1089 \u1087 \u1077 \u1096 \u1085 \u1072 . \u1058 \u1077 \u1087 \u1077 \u1088 \u1100  \u1074 \u1086 \u1081 \u1076 \u1080 \u1090 \u1077 .")\
            return redirect(url_for("login"))\
        return render_template("register.html", form=form)\
\
    @app.route("/login", methods=["GET", "POST"])\
    def login():\
        if current_user.is_authenticated:\
            return redirect(url_for("index"))\
        form = LoginForm()\
        if form.validate_on_submit():\
            user = User.query.filter_by(username=form.username.data).first()\
            if user and check_password_hash(user.password_hash, form.password.data):\
                login_user(user)\
                flash("\uc0\u1042 \u1099  \u1074 \u1086 \u1096 \u1083 \u1080  \u1074  \u1089 \u1080 \u1089 \u1090 \u1077 \u1084 \u1091 .")\
                next_page = request.args.get("next")\
                return redirect(next_page or url_for("index"))\
            flash("\uc0\u1053 \u1077 \u1074 \u1077 \u1088 \u1085 \u1086 \u1077  \u1080 \u1084 \u1103  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103  \u1080 \u1083 \u1080  \u1087 \u1072 \u1088 \u1086 \u1083 \u1100 .")\
        return render_template("login.html", form=form)\
\
    @app.route("/logout")\
    @login_required\
    def logout():\
        logout_user()\
        flash("\uc0\u1042 \u1099  \u1074 \u1099 \u1096 \u1083 \u1080  \u1080 \u1079  \u1089 \u1080 \u1089 \u1090 \u1077 \u1084 \u1099 .")\
        return redirect(url_for("index"))\
\
    @app.route("/post/create", methods=["GET", "POST"])\
    @login_required\
    def create_post():\
        form = PostForm()\
        if form.validate_on_submit():\
            post = Post(\
                title=form.title.data,\
                body=form.body.data,\
                author=current_user,\
                is_public=form.is_public.data,\
                request_only=form.request_only.data,\
            )\
            tags_raw = form.tags.data or ""\
            tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]\
            for name in tag_names:\
                tag = Tag.query.filter_by(name=name).first()\
                if not tag:\
                    tag = Tag(name=name)\
                    db.session.add(tag)\
                post.tags.append(tag)\
            db.session.add(post)\
            db.session.commit()\
            flash("\uc0\u1055 \u1086 \u1089 \u1090  \u1089 \u1086 \u1079 \u1076 \u1072 \u1085 .")\
            return redirect(url_for("post_detail", post_id=post.id))\
        return render_template("create_post.html", form=form, title="\uc0\u1057 \u1086 \u1079 \u1076 \u1072 \u1085 \u1080 \u1077  \u1087 \u1086 \u1089 \u1090 \u1072 ")\
\
    @app.route("/post/<int:post_id>", methods=["GET", "POST"])\
    def post_detail(post_id):\
        post = Post.query.get_or_404(post_id)\
        if not post.is_public and (not current_user.is_authenticated or post.author != current_user):\
            if not post.request_only:\
                abort(403)\
            flash("\uc0\u1069 \u1090 \u1086  \u1089 \u1082 \u1088 \u1099 \u1090 \u1099 \u1081  \u1087 \u1086 \u1089 \u1090 . \u1044 \u1086 \u1089 \u1090 \u1091 \u1087  \u1090 \u1086 \u1083 \u1100 \u1082 \u1086  \u1087 \u1086  \u1079 \u1072 \u1087 \u1088 \u1086 \u1089 \u1091  \u1072 \u1074 \u1090 \u1086 \u1088 \u1091 .")\
        form = CommentForm()\
        if form.validate_on_submit():\
            if not current_user.is_authenticated:\
                flash("\uc0\u1044 \u1083 \u1103  \u1082 \u1086 \u1084 \u1084 \u1077 \u1085 \u1090 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1103  \u1085 \u1077 \u1086 \u1073 \u1093 \u1086 \u1076 \u1080 \u1084 \u1086  \u1074 \u1086 \u1081 \u1090 \u1080 .")\
                return redirect(url_for("login"))\
            comment = Comment(body=form.body.data, author=current_user, post=post)\
            db.session.add(comment)\
            db.session.commit()\
            flash("\uc0\u1050 \u1086 \u1084 \u1084 \u1077 \u1085 \u1090 \u1072 \u1088 \u1080 \u1081  \u1076 \u1086 \u1073 \u1072 \u1074 \u1083 \u1077 \u1085 .")\
            return redirect(url_for("post_detail", post_id=post.id))\
        comments = post.comments.order_by(Comment.created_at.asc())\
        return render_template("post_detail.html", post=post, form=form, comments=comments)\
\
    @app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])\
    @login_required\
    def edit_post(post_id):\
        post = Post.query.get_or_404(post_id)\
        if post.author != current_user:\
            abort(403)\
        form = PostForm(obj=post)\
        if form.validate_on_submit():\
            post.title = form.title.data\
            post.body = form.body.data\
            post.is_public = form.is_public.data\
            post.request_only = form.request_only.data\
\
            post.tags.clear()\
            tags_raw = form.tags.data or ""\
            tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]\
            for name in tag_names:\
                tag = Tag.query.filter_by(name=name).first()\
                if not tag:\
                    tag = Tag(name=name)\
                    db.session.add(tag)\
                post.tags.append(tag)\
\
            db.session.commit()\
            flash("\uc0\u1055 \u1086 \u1089 \u1090  \u1086 \u1073 \u1085 \u1086 \u1074 \u1083 \u1105 \u1085 .")\
            return redirect(url_for("post_detail", post_id=post.id))\
\
        form.tags.data = ", ".join([t.name for t in post.tags])\
        return render_template("create_post.html", form=form, title="\uc0\u1056 \u1077 \u1076 \u1072 \u1082 \u1090 \u1080 \u1088 \u1086 \u1074 \u1072 \u1085 \u1080 \u1077  \u1087 \u1086 \u1089 \u1090 \u1072 ")\
\
    @app.route("/post/<int:post_id>/delete", methods=["POST"])\
    @login_required\
    def delete_post(post_id):\
        post = Post.query.get_or_404(post_id)\
        if post.author != current_user:\
            abort(403)\
        db.session.delete(post)\
        db.session.commit()\
        flash("\uc0\u1055 \u1086 \u1089 \u1090  \u1091 \u1076 \u1072 \u1083 \u1105 \u1085 .")\
        return redirect(url_for("my_posts"))\
\
    @app.route("/my-posts")\
    @login_required\
    def my_posts():\
        posts = Post.query.filter_by(author=current_user).order_by(Post.created_at.desc())\
        return render_template("my_posts.html", posts=posts)\
\
    @app.route("/user/<int:user_id>/follow", methods=["POST"])\
    @login_required\
    def follow(user_id):\
        user = User.query.get_or_404(user_id)\
        if user == current_user:\
            flash("\uc0\u1053 \u1077 \u1083 \u1100 \u1079 \u1103  \u1087 \u1086 \u1076 \u1087 \u1080 \u1089 \u1072 \u1090 \u1100 \u1089 \u1103  \u1085 \u1072  \u1089 \u1072 \u1084 \u1086 \u1075 \u1086  \u1089 \u1077 \u1073 \u1103 .")\
        else:\
            current_user.follow(user)\
            db.session.commit()\
            flash(f"\uc0\u1042 \u1099  \u1087 \u1086 \u1076 \u1087 \u1080 \u1089 \u1072 \u1083 \u1080 \u1089 \u1100  \u1085 \u1072  \{user.username\}.")\
        return redirect(request.referrer or url_for("index"))\
\
    @app.route("/user/<int:user_id>/unfollow", methods=["POST"])\
    @login_required\
    def unfollow(user_id):\
        user = User.query.get_or_404(user_id)\
        if user == current_user:\
            flash("\uc0\u1053 \u1077 \u1083 \u1100 \u1079 \u1103  \u1086 \u1090 \u1087 \u1080 \u1089 \u1072 \u1090 \u1100 \u1089 \u1103  \u1086 \u1090  \u1089 \u1072 \u1084 \u1086 \u1075 \u1086  \u1089 \u1077 \u1073 \u1103 .")\
        else:\
            current_user.unfollow(user)\
            db.session.commit()\
            flash(f"\uc0\u1042 \u1099  \u1086 \u1090 \u1087 \u1080 \u1089 \u1072 \u1083 \u1080 \u1089 \u1100  \u1086 \u1090  \{user.username\}.")\
        return redirect(request.referrer or url_for("index"))\
\
    @app.route("/subscriptions")\
    @login_required\
    def subscriptions_feed():\
        posts = (\
            Post.query.join(User, Post.user_id == User.id)\
            .filter(User.id.in_([u.id for u in current_user.followed]))\
            .filter(Post.is_public == True)\
            .order_by(Post.created_at.desc())\
        )\
        return render_template("subscriptions.html", posts=posts)\
\
    return app\
\
\
if __name__ == "__main__":\
    app = create_app()\
    app.run(debug=True)\
}