from flask_restful import Resource
from app import db


class APIResource(Resource):

    def get_one(self, field, filters=[]):
        return db.session.query(*field).filter(*filters).first()

    def get_all_one(self, filter, param):
        return self.model.query.filter(filter == param).first()

    # 增加单个操作
    def increase_one(self, **kwargs):
        db.session.add(self.model(**kwargs))
        db.session.commit()

    # 删除单个操作
    def delete_one(self, param, id):
        self.model.query.filter(param == id
                                ).delete()
        db.session.commit()

    # 修改单个操作
    def update_one(self, c_id, **kwargs):
        self.model.query.filter(self.model.id == c_id
                                ).update(kwargs)
        db.session.commit()

    # 展示全部
    def query_select(self, field, filters=[], order=[]):
        data = db.session.query(*field).filter(*filters).order_by(*order)

        return data.all()

    # 查询搜索(分页)
    def query_page(self, field, filters: list = [], page: int = 1, per_page: int = 15, order: list = []) -> tuple:
        collects = db.session.query(*field).filter(*filters).order_by(*order)

        collects = collects.paginate(
            page=page,
            per_page=per_page)
        return collects.items, {"pages": collects.pages, "total": collects.total}
