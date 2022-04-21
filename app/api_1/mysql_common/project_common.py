from sqlalchemy import func

from app import db
from app.models.project_model import Project


class ProjectCommon:

    # project状态统计
    @staticmethod
    def status_census():
        status = db.session.query(func.count(Project.status)).group_by(Project.status).all()

        return status
