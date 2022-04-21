import json

from app import db
from app.models import format_fields


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.String(36), primary_key=True, info='id')
    project_name = db.Column(db.String(50), nullable=False, info='项目名')
    introduction = db.Column(db.String(255), info='项目介绍')
    status = db.Column(db.Integer, nullable=False, info='0 等待 1 进行 2 完成')
    create_time = db.Column(db.DateTime, nullable=False, info='时间')
    progress = db.Column(db.Text, nullable=False, info='进度')
    clone_url = db.Column(db.String(100), info='克隆URL')
    git_url = db.Column(db.String(100), info='git克隆URL')
    github_url = db.Column(db.String(100), info='gihub链接')

    def toDict(self):
        dic = self.__dict__
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        if dic["create_time"]:
            dic["create_time"] = str(dic["create_time"])
        if dic["progress"]:
            dic["progress"] = json.loads(dic["progress"])

        return dic


# 格式化字段
project_all = format_fields(Project)
