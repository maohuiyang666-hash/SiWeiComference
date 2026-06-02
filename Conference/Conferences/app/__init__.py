import os
from urllib import parse

from flask import Flask

from . import conf


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CONFERENCE_SECRET_KEY', 'dev-secret-change-me')

DIALECT = 'mssql'
DRIVER = 'pymssql'
USERNAME = conf.db_user
PASSWORD = parse.quote_plus(conf.db_password)
HOST = conf.db_host
PORT = conf.db_port
DATABASE = conf.db_database
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI


@app.context_processor
def gettype():
    model_types = {
        '1': '图像分类',
        '2': '语义分割',
        '3': '目标检测',
        '4': '图像生成',
        '5': '语言建模',
        '6': '问答',
        '7': '机器翻译',
        '8': '文本生成',
    }
    return dict(model_type=model_types)


from .home import home as home_blueprint

app.register_blueprint(home_blueprint)
