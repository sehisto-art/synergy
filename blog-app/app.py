import os
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Post, Tag, Comment
from forms import RegisterForm, LoginForm, PostForm, CommentForm


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        tag_name = request.args.get("tag")
        if tag_name:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag:
                posts = tag.posts.filter(Post.is_public == True).order_by(Post.created_at.desc())
            else:
                posts = []
        else:
            posts = Post.query.filter_by(is_public=True).order_by(Post.created_at.desc())
        return render_template("index.html", posts=posts, tag_name=tag_name)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = RegisterForm()
        if form.validate_on_submit():
            if User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first():
                flash("Пользователь с таким именем или email уже существует.")
                return redirect(url_for("register"))
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
            )
            db.session.add(user)
            db.session.commit()
            flash("Регистрация успешна. Теперь войдите.")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Вы вошли в систему.")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("index"))
            flash("Неверное имя пользователя или пароль.")
        return render_template("login.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Вы вышли из системы.")
        return redirect(url_for("index"))

    @app.route("/post/create", methods=["GET", "POST"])
    @login_required
    def create_post():
        form = PostForm()
        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                body=form.body.data,
                author=current_user,
                is_public=form.is_public.data,
                request_only=form.request_only.data,
            )
            tags_raw = form.tags.data or ""
            tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]
            for name in tag_names:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                post.tags.append(tag)
            db.session.add(post)
            db.session.commit()
            flash("Пост создан.")
            return redirect(url_for("post_detail", post_id=post.id))
        return render_template("create_post.html", form=form, title="Создание поста")

    @app.route("/post/<int:post_id>", methods=["GET", "POST"])
    def post_detail(post_id):
        post = Post.query.get_or_404(post_id)
        if not post.is_public and (not current_user.is_authenticated or post.author != current_user):
            if not post.request_only:
                abort(403)
            flash("Это скрытый пост. Доступ только по запросу автору.")
        form = CommentForm()
        if form.validate_on_submit():
            if not current_user.is_authenticated:
                flash("Для комментирования необходимо войти.")
                return redirect(url_for("login"))
            comment = Comment(body=form.body.data, author=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            flash("Комментарий добавлен.")
            return redirect(url_for("post_detail", post_id=post.id))
        comments = post.comments.order_by(Comment.created_at.asc())
        return render_template("post_detail.html", post=post, form=form, comments=comments)

    @app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        form = PostForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            post.is_public = form.is_public.data
            post.request_only = form.request_only.data

            post.tags.clear()
            tags_raw = form.tags.data or ""
            tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]
            for name in tag_names:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                post.tags.append(tag)

            db.session.commit()
            flash("Пост обновлён.")
            return redirect(url_for("post_detail", post_id=post.id))

        form.tags.data = ", ".join([t.name for t in post.tags])
        return render_template("create_post.html", form=form, title="Редактирование поста")

    @app.route("/post/<int:post_id>/delete", methods=["POST"])
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash("Пост удалён.")
        return redirect(url_for("my_posts"))

    @app.route("/my-posts")
    @login_required
    def my_posts():
        posts = Post.query.filter_by(author=current_user).order_by(Post.created_at.desc())
        return render_template("my_posts.html", posts=posts)

    @app.route("/user/<int:user_id>/follow", methods=["POST"])
    @login_required
    def follow(user_id):
        user = User.query.get_or_404(user_id)
        if user == current_user:
            flash("Нельзя подписаться на самого себя.")
        else:
            current_user.follow(user)
            db.session.commit()
            flash(f"Вы подписались на {user.username}.")
        return redirect(request.referrer or url_for("index"))

    @app.route("/user/<int:user_id>/unfollow", methods=["POST"])
    @login_required
    def unfollow(user_id):
        user = User.query.get_or_404(user_id)
        if user == current_user:
            flash("Нельзя отписаться от самого себя.")
        else:
            current_user.unfollow(user)
            db.session.commit()
            flash(f"Вы отписались от {user.username}.")
        return redirect(request.referrer or url_for("index"))

    @app.route("/subscriptions")
    @login_required
    def subscriptions_feed():
        posts = (
            Post.query.join(User, Post.user_id == User.id)
            .filter(User.id.in_([u.id for u in current_user.followed]))
            .filter(Post.is_public == True)
            .order_by(Post.created_at.desc())
        )
        return render_template("subscriptions.html", posts=posts)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
