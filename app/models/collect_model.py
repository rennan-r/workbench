from app import db


# flask-sqlacodegen mysql+pymysql://root:ztac123456@192.168.99.100:3003/wus --flask


class CollectClas(db.Model):
    __tablename__ = 'collect_class'

    id = db.Column(db.String(36), primary_key=True)
    class_name = db.Column(db.String(10), nullable=False, info='分类名称')

    def toDict(self):
        dic = self.__dict__
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        return dic


class CollectEntry(db.Model):
    __tablename__ = 'collect_entry'

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(100), nullable=False, info='标题')
    introduction = db.Column(db.String(200), info='简介')
    content = db.Column(db.Text, nullable=False, info='内容')
    markdown = db.Column(db.Text, nullable=False, info='markdown')
    is_top = db.Column(db.Integer, nullable=False, info='是否置顶')
    c_class = db.Column(db.String(36), nullable=False, info='分类')
    create_time = db.Column(db.DateTime, nullable=False, info='创建时间')

    def toDict(self):
        dic = self.__dict__
        if "_sa_instance_state" in dic: del dic["_sa_instance_state"]
        if dic["create_time"]: dic["create_time"] = str(dic["create_time"])
        if dic["c_class"]: dic["c_class"] = \
            db.session.query(CollectClas.class_name).filter(CollectClas.id == dic["c_class"]).first()[0]
        return dic


collect_list = {"id": CollectEntry.id, "title": CollectEntry.title, "is_top": CollectEntry.is_top,
                "c_class": CollectClas.class_name,
                "introduction": CollectEntry.introduction, "markdown": CollectEntry.markdown}

collect_top_list = {"id": CollectEntry.id, "title": CollectEntry.title,
                    "c_class": CollectClas.class_name}
collect_entry = {"title": CollectEntry.title, "introduction": CollectEntry.introduction,
                 "content": CollectEntry.content,
                 "create_time": CollectEntry.create_time, "c_class": CollectClas.class_name,
                 "markdown": CollectEntry.markdown}



