from app.api_1 import args_parse
from app.api_1.mysql_common.api_common import APIResource
from app.api_1.mysql_common.collect_common import CollectCommon
from app.lib.APIException import ApiException
from app.lib.Wus_Response import return_response, return_response_page
from app.lib.constant import CollectConstant
from app.models.collect_model import CollectEntry, CollectClas, collect_list, collect_top_list, collect_entry
from app.util.common_util import Common


class CollectEt(APIResource):
    model = CollectEntry

    @args_parse(schemy={
        "title": {"type": str, "required": True},
        "introduction": {"type": str, "required": True},
        "content": {"type": str, "required": True},
        "markdown": {"type": str, "required": True},
        "c_class": {"type": str, "required": True},
        "is_top": {"type": int, "required": True},
    })  # 添加搜藏条目
    def post(self, title, introduction, content, markdown, c_class, is_top):
        if self.get_one([self.model.id], [self.model.title == title]):
            raise ApiException(*CollectConstant.REPEAT_ET)
        self.increase_one(id=Common.get_a_uuid(), title=title, introduction=introduction,
                          content=content, markdown=markdown,
                          is_top=is_top, c_class=c_class, create_time=Common.get_now_time())

        return return_response(message="添加成功")

    @args_parse(schemy={
        "title": {"type": str, "required": False},
        "content": {"type": str, "required": False},
        "c_class": {"type": str, "required": False},
        "interval_time": {"type": str, "required": False},
        "page": {"type": int, "required": True, "default": 1},
        "per_page": {"type": int, "required": True, "default": 10},
        "is_top": {"type": int, "required": False}
    })  # 搜索搜藏条目
    def get(self, page, per_page, is_top=1, title=None, content=None, c_class=None, interval_time=None):
        filters = []
        if title:
            filters.append(CollectEntry.title.ilike("%{}%".format(title)))
        if is_top:
            filters.append(CollectEntry.is_top == is_top)
        if content:
            filters.append(CollectEntry.content.ilike("%{}%".format(content)))
        if c_class:
            filters.append(CollectEntry.c_class.in_(c_class.split(",")))
        if interval_time:
            filters.append(CollectEntry.create_time.between(*interval_time.split("=")))

        # 是否置顶数据
        if is_top == 1:
            field = collect_top_list
        else:
            field = collect_list
        data, meta = CollectCommon.query_collect(filters=filters, page=page, per_page=per_page, field=field.values())
        return return_response_page(data=Common.json_orm_result(field.keys(), data), page=page, per_page=per_page,
                                    **meta)


class CollectObjectEt(APIResource):
    model = CollectEntry

    @args_parse(schemy={
        "title": {"type": str, "required": True},
        "introduction": {"type": str, "required": True},
        "content": {"type": str, "required": True},
        "c_class": {"type": str, "required": True}
    })  # 修改搜藏条目
    def put(self, c_id, title, introduction, content, c_class):
        self.update_one(c_id, title=title, introduction=introduction, content=content,
                        c_class=c_class)

        return return_response()

    # 删除
    def delete(self, c_id):
        self.delete_one(self.model.id, c_id)

        return return_response(message="删除成功")

    # 单个收藏条目
    def get(self, c_id):
        collect = collect_entry
        collect["c_class"] = CollectEntry.c_class
        collect["class_name"] = CollectClas.class_name
        col = CollectCommon.show_collect(c_id, collect.values())
        data = Common.json_orm_result(collect.keys(), data=col)[0]
        data["create_time"] = str(data["create_time"])
        return return_response(data=data)


class CollectClass(APIResource):
    model = CollectClas

    # 获取分类
    def get(self):
        data = self.query_select([CollectClas.id, CollectClas.class_name])

        return return_response(data=Common.json_orm_result(row=("value", "label"), data=data))

    @args_parse(schemy={
        "class_name": {"type": str, "required": True}
    })  # 添加分类
    def post(self, class_name):
        if self.get_one([self.model.id], [self.model.class_name == class_name]):
            raise ApiException(*CollectConstant.REPEAT_CLASS)
        c_id = Common.get_a_uuid()
        print(c_id)
        self.increase_one(id=c_id, class_name=class_name)
        return return_response(data={'c_id': c_id, 'class_name': class_name}, message="添加成功")

    @args_parse(schemy={
        "c_id": {"type": str, "required": True}
    })  # 删除分类
    def delete(self, c_id):
        # if CollectCommon.query_collect(field=(CollectEntry.id), filters=[CollectEntry.c_class == c_id]):
        #     raise ApiException(*CollectConstant.DELETE_ET)
        self.delete_one(self.model.id, c_id)
        return return_response()

    @args_parse(schemy={
        "c_id": {"type": str, "required": True},
        "class_name": {"type": str, "required": True}
    })  # 修改分类
    def put(self, c_id, class_name):
        self.update_one(c_id, class_name=class_name)
        return return_response()


# collect操作
class CollectOper(APIResource):
    model = CollectEntry

    # 置顶
    @args_parse(schemy={
        "is_top": {"type": int, "required": True}
    })
    def get(self, c_id, is_top):
        self.update_one(c_id, is_top=is_top)

        return return_response()
