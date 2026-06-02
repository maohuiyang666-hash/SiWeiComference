from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib import parse

app = Flask(__name__)

DIALECT = 'mssql'
DRIVER = 'pymssql'
USERNAME = 'sa'
PASSWORD = parse.quote_plus('Iotlab2019@217')
HOST = '127.0.0.1' #'139.196.146.45'
PORT = '1433'  #'22'
DATABASE = 'test'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(
    DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE
)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

@app.context_processor
def gettype():
    type ={
        '1': '图像分类',
        '2': '语义分割',
        '3': '目标检测',
        '4': '图像生成',
        '5': '语言建模',
        '6': '问答',
        '7': '机器翻译',
        '8': '文本生成'
    }
    return dict(model_type = type)

from .home import home as home_blueprint
from .sqlConnect import Mssql


app.register_blueprint(home_blueprint)