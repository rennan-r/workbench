import json

from sqlalchemy import case, func

from app.api_1 import args_parse
from app.api_1.mysql_common.api_common import APIResource
from app.api_1.mysql_common.project_common import ProjectCommon
from app.lib.APIException import ApiException
from app.lib.constant import ProjectConstant, defult
from app.lib.github import github
from app.models.project_model import Project, project_all
from app.util.common_util import Common
from app.lib.Wus_Response import return_response, return_response_page


class ProjectAdmin(APIResource):
    model = Project

    @args_parse(schemy={
        "project_name": {"type": str, "required": False},
        "status": {"type": str, "required": False},
        "page": {"type": int, "required": False},
        "per_page": {"type": int, "required": False},
    })  # 获取项目
    def get(self, project_name, status, page, per_page):
        filters = []
        if project_name:
            filters.append(self.model.project_name.like("%{}%".format(project_name)))
        if status:
            filters.append(self.model.status == status)
        data, meta = self.query_page(field=project_all.values(), filters=filters, page=page, per_page=per_page)

        def func(data):

            data["create_time"] = str(data["create_time"])
            progress = json.loads(data["progress"])
            data["percent"] = sum([i["value"] for i in progress]) / len(progress)
            data["names"] = [i['label'] for i in progress]
            data["keys"] = list(range(len(progress)))
            return data

        return return_response_page(data=Common.json_orm_result(project_all.keys(), data, func), page=page,
                                    per_page=per_page,
                                    **meta)

    @args_parse(schemy={
        "project_name": {"type": str, "required": True},
        "introduction": {"type": str, "required": False},
        "progress": {"type": Common.list_type, "required": True, "location": 'json'},
        "relevance": {"type": bool, "required": False, "default": False}
    })  # 创建项目
    def post(self, project_name, introduction, progress, relevance):
        project = self.get_one(filter=self.model.project_name, param=project_name)
        # 项目不能重复
        if project:
            raise ApiException(*ProjectConstant.REPEAT_PROJECT)
        check, data = github.check_repository(project_name)
        if not relevance:
            # 不合并项目就创建储存库
            if check:
                raise ApiException(*ProjectConstant.REPEAT_PROJECT)
            ok, data = github.create_repository(project_name)
            if not ok:
                raise ApiException(*defult)

        # 合并就只创建项目
        project_id = Common.get_a_uuid()
        self.increase_one(id=project_id, project_name=project_name, introduction=introduction, status=0,
                          create_time=data["created_at"][:-1].replace("T", " "),
                          progress=json.dumps(progress), clone_url=data["clone_url"], git_url=data["git_url"],
                          github_url=data["html_url"])

        return return_response(data={'project_id': project_id}, message="添加成功")

    def put(self):
        field = [
            func.count(case([(self.model.status == 0, self.model.status)])),
            func.count(case([(self.model.status == 1, self.model.status)])),
            func.count(case([(self.model.status == 2, self.model.status)]))
        ]
        data = self.query_select(field)
        if data:
            data = dict(zip(["wait", "runing", "complete"], data[0]))
        return return_response(data=data)


class ProjectOper(APIResource):
    model = Project

    def delete(self, project_id):
        if not self.get_one(self.model.id, project_id):
            raise ApiException(*ProjectConstant.NOT_PROJECT)
        self.delete_one(self.model.id, project_id)
        return return_response()

    @args_parse(schemy={
        "introduction": {"type": str, "required": False},
        "progress": {"type": Common.dict_type, "required": True}
    })  # 修改项目详情
    def put(self, project_id, introduction, progress):
        self.update_one(project_id, introduction=introduction, progress=json.dumps(progress))
        return return_response()
