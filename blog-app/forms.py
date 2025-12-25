{\rtf1\ansi\ansicpg1251\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask_wtf import FlaskForm\
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField\
from wtforms.validators import DataRequired, Email, Length, EqualTo\
\
\
class RegisterForm(FlaskForm):\
    username = StringField("\uc0\u1048 \u1084 \u1103  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103 ", validators=[DataRequired(), Length(min=3, max=64)])\
    email = StringField("Email", validators=[DataRequired(), Email()])\
    password = PasswordField("\uc0\u1055 \u1072 \u1088 \u1086 \u1083 \u1100 ", validators=[DataRequired(), Length(min=6)])\
    password2 = PasswordField("\uc0\u1055 \u1086 \u1074 \u1090 \u1086 \u1088 \u1080 \u1090 \u1077  \u1087 \u1072 \u1088 \u1086 \u1083 \u1100 ", validators=[DataRequired(), EqualTo("password")])\
    submit = SubmitField("\uc0\u1047 \u1072 \u1088 \u1077 \u1075 \u1080 \u1089 \u1090 \u1088 \u1080 \u1088 \u1086 \u1074 \u1072 \u1090 \u1100 \u1089 \u1103 ")\
\
\
class LoginForm(FlaskForm):\
    username = StringField("\uc0\u1048 \u1084 \u1103  \u1087 \u1086 \u1083 \u1100 \u1079 \u1086 \u1074 \u1072 \u1090 \u1077 \u1083 \u1103 ", validators=[DataRequired()])\
    password = PasswordField("\uc0\u1055 \u1072 \u1088 \u1086 \u1083 \u1100 ", validators=[DataRequired()])\
    submit = SubmitField("\uc0\u1042 \u1086 \u1081 \u1090 \u1080 ")\
\
\
class PostForm(FlaskForm):\
    title = StringField("\uc0\u1047 \u1072 \u1075 \u1086 \u1083 \u1086 \u1074 \u1086 \u1082 ", validators=[DataRequired(), Length(max=140)])\
    body = TextAreaField("\uc0\u1058 \u1077 \u1082 \u1089 \u1090 ", validators=[DataRequired()])\
    tags = StringField("\uc0\u1058 \u1077 \u1075 \u1080  (\u1095 \u1077 \u1088 \u1077 \u1079  \u1079 \u1072 \u1087 \u1103 \u1090 \u1091 \u1102 )")\
    is_public = BooleanField("\uc0\u1055 \u1091 \u1073 \u1083 \u1080 \u1095 \u1085 \u1099 \u1081  \u1087 \u1086 \u1089 \u1090 ")\
    request_only = BooleanField("\uc0\u1057 \u1082 \u1088 \u1099 \u1090 \u1099 \u1081  \u1087 \u1086 \u1089 \u1090  (\u1090 \u1086 \u1083 \u1100 \u1082 \u1086  \u1087 \u1086  \u1079 \u1072 \u1087 \u1088 \u1086 \u1089 \u1091 )")\
    submit = SubmitField("\uc0\u1057 \u1086 \u1093 \u1088 \u1072 \u1085 \u1080 \u1090 \u1100 ")\
\
\
class CommentForm(FlaskForm):\
    body = TextAreaField("\uc0\u1050 \u1086 \u1084 \u1084 \u1077 \u1085 \u1090 \u1072 \u1088 \u1080 \u1081 ", validators=[DataRequired(), Length(max=500)])\
    submit = SubmitField("\uc0\u1054 \u1090 \u1087 \u1088 \u1072 \u1074 \u1080 \u1090 \u1100 ")\
}