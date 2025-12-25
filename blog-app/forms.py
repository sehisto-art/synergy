from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=140)])
    body = TextAreaField("Текст", validators=[DataRequired()])
    tags = StringField("Теги (через запятую)")
    is_public = BooleanField("Публичный пост")
    request_only = BooleanField("Скрытый пост (только по запросу)")
    submit = SubmitField("Сохранить")


class CommentForm(FlaskForm):
    body = TextAreaField("Комментарий", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Отправить")
