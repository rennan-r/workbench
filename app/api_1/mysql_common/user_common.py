from app import db
from app.models.user_model import User


class UserCommon:

    # 添加用户
    @staticmethod
    def register(**kwargs):
        db.session.add(User(**kwargs))
        db.session.commit()

    # 用户是否存在
    @staticmethod
    def user(pl: str, user: str):
        return User.query.filter(getattr(User, pl) == user).first()


