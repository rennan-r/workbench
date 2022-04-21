# coding: utf-8
from app import db

# flask-sqlacodegen mysql+pymysql://root:ztac123456@192.168.99.100:3003/wus --flask

class User(db.Model):
    __tablename__ = 'user'

    u_id = db.Column(db.String(36), primary_key=True, info='用户id')
    username = db.Column(db.String(20), nullable=False, info='用户名')
    password = db.Column(db.Text, nullable=False, info='用户密码')
    create_time = db.Column(db.DateTime, nullable=False, info='创建时间')
    approve = db.Column(db.Integer, nullable=False, info='是否审批0 否 1 是')

