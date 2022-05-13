import hashlib
import json
import os

from sqlalchemy import case, func

from app.api_1 import args_parse
from app.api_1.mysql_common.api_common import APIResource
from app.api_1.mysql_common.project_common import ProjectCommon
from app.lib.APIException import ApiException
from app.lib.constant import ProjectConstant, defult
from app.lib.github import github
from app.models.project_model import Project, project_all, Commit, commit_all, project_status, ProjectEvent, event_all
from app.util.common_util import Common
from app.lib.Wus_Response import return_response, return_response_page


class ProjectAPIResource(APIResource):
    model = Project
    pass


class ProjectAdmin(ProjectAPIResource):

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
        data, meta = self.query_page(field=project_all.values(), filters=filters, page=page, per_page=per_page,
                                     order=[self.model.create_time.desc(), self.model.status.asc()])

        def func(data):

            data["create_time"] = str(data["create_time"])
            progress = json.loads(data["progress"])
            data["percent"] = sum([i["value"] for i in progress]) / len(progress) * 100
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
        project = self.get_one([self.model.id], [self.model.project_name == project_name])
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
        project_id = Common.get_a_uuid()
        if not data:
            raise ApiException(*defult)
        # 合并就只创建项目
        self.increase_one(id=project_id, project_name=project_name, introduction=introduction, status=0,
                          create_time=Common.github_time_format(data["created_at"]),
                          progress=json.dumps(progress), clone_url=data["clone_url"], git_url=data["git_url"],
                          github_url=data["html_url"])
        commits = github.lay_version(project_id, project_name)
        if commits:
            # 提交记录
            ProjectCommon.create_commits(commits)
        return return_response(data={'project_id': project_id}, message="添加成功")

    # 项目状态详情
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


class ProjectOper(ProjectAPIResource):

    # 项目详情
    def get(self, project_id):
        project = self.get_all_one(self.model.id, project_id)
        # # 返回github webhook回调地址
        hook_url = Common.github_hook_url(project.project_name)
        project = project.toDict()
        project["hook_url"] = hook_url
        project["status"] = project_status[str(project["status"])]
        for index, value in enumerate(project["progress"]):
            if value["value"] == 0:
                project["current"] = index
                break
            elif index + 1 == len(project["progress"]):
                project["current"] = len(project["progress"])
        return return_response(data=project)

    @args_parse(schemy={
        "oper": {"type": str, "required": True}  # 0 or 1
    })  # 进度条修改
    def post(self, project_id, oper):
        dic = {}
        if oper not in ["-1", "1"]:
            raise ApiException(*defult)
        progress = json.loads(self.get_one([self.model.progress], [self.model.id == project_id])[0])
        progress_index = None
        len_progress = len(progress)
        # 计算达到的进度下标
        for index, value in enumerate(progress):
            if value["value"] == 0:
                progress_index = index
                break
            elif index + 1 == len_progress:
                progress_index = index + 1

        # 进行下一步或上一步操作
        if oper == "1":
            if progress_index == len_progress:
                raise ApiException(*defult)
            progress[progress_index]["value"] = 1
            if progress_index == len_progress - 1:
                dic["status"] = 2
        else:
            if progress_index - 1 == -1:
                raise ApiException(*defult)
            progress[progress_index - 1]["value"] = 0

            if progress_index == len_progress:
                dic["status"] = 1

        dic["progress"] = json.dumps(progress)
        self.update_one(project_id, **dic)

        return return_response(data={"current": progress_index + int(oper), "status": dic.get("status")})

    # 删除
    def delete(self, project_id):
        project = self.get_one([self.model.id, self.model.project_name], [self.model.id == project_id])
        if not project:
            raise ApiException(*ProjectConstant.NOT_PROJECT)
        if not github.delete_repository(project['project_name']):
            raise ApiException(*defult)
        self.delete_one(self.model.id, project_id)
        return return_response()

    @args_parse(schemy={
        "introduction": {"type": str, "required": False},
        "progress": {"type": Common.list_type, "required": True, "location": 'json'}
    })  # 修改项目详情
    def put(self, project_id, introduction, progress):
        self.update_one(project_id, introduction=introduction, progress=json.dumps(progress))
        return return_response()


class ProjectCommit(ProjectAPIResource):
    model = Commit

    @args_parse(schemy={
        "message": {"type": str, "required": False},
        "page": {"type": int, "required": False},
        "per_page": {"type": int, "required": False}
    })  # 获取项目
    def get(self, project_id, message, page, per_page):
        filters = [self.model.project_id == project_id]
        if message:
            filters.append(self.model.message.like("%{}%".format(message)))

        data, meta = self.query_page(field=commit_all.values(), filters=filters, page=page, per_page=per_page,
                                     order=[self.model.commit_time.desc()])

        def func(data):
            data["commit_time"] = str(data["commit_time"])

            return data

        return return_response_page(data=Common.json_orm_result(commit_all.keys(), data, func), page=page,
                                    per_page=per_page,
                                    **meta)


class ProjectHookToken(ProjectAPIResource):

    def get(self):
        token = hashlib.sha1(os.urandom(24)).hexdigest()

        return return_response(data={"token": token})


class ProjectCommitOper(APIResource):
    model = Commit

    # webhook 回调
    def post(self):
        pass


class ProjectEventOper(APIResource):
    model = ProjectEvent

    @args_parse(schemy={
        "name": {"type": str, "required": False},
    })  # 添加事件
    def post(self, project_id, name):
        id, create_time = Common.get_a_uuid(), Common.get_now_time()
        self.increase_one(id=id, project_id=project_id, name=name, create_time=create_time)

        return return_response(data={
            "id": id,
            "name": name,
            "create_time": str(create_time)
        })

    # 获取事件
    def get(self, project_id):
        event = self.query_select(event_all.values(), [self.model.project_id == project_id],
                                  [self.model.create_time.desc()])

        def func(data):
            data["create_time"] = str(data["create_time"])

            return data

        return return_response(data=Common.json_orm_result(event_all.keys(), event, func=func))

    @args_parse(schemy={
        "event_id": {"type": str, "required": False},
    })  # 完成事件
    def delete(self, project_id, event_id):
        self.delete_one(self.model.id, event_id)
        return return_response()
