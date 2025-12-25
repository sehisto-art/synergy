import os\
\
BASE_DIR = os.path.abspath(os.path.dirname(__file__))\
\
class Config:\
    SECRET_KEY = "change_me_in_production"\
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "blog.db")\
    SQLALCHEMY_TRACK_MODIFICATIONS = False\
}
