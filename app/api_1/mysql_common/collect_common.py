from app import db

from app.models.collect_model import CollectEntry, CollectClas


class CollectCommon:

    # 查询搜索条目(分页)
    @staticmethod
    def query_collect(field, filters: list, page: int = 1, per_page: int = 15) -> tuple:
        collects = db.session.query(*field).filter(*filters).join(CollectClas,
                                                                  CollectClas.id == CollectEntry.c_class).paginate(
            page=page,
            per_page=per_page)
        return collects.items, {"pages": collects.pages, "total": collects.total}

    # 获取单个收藏
    @staticmethod
    def show_collect(c_id, field):
        res = db.session.query(*field).filter(CollectEntry.id == c_id). \
            join(CollectClas, CollectClas.id == CollectEntry.c_class).all()

        return res


