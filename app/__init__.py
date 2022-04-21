from flask import Flask
from flask_restful import Api
from app.route import Url
from app.conf.app_config import AppConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(AppConfig)
db = SQLAlchemy(app=app)

api = Api(app)
Url(api).add_url()

# 创建数据表
# db.create_all()
