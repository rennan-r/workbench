class Url:
    def __init__(self, api):
        self.api = api

    # 用户接口注册
    def user(self):
        from app.api_1.user import UserLogin, UserRegister
        self.api.add_resource(UserLogin, '/login')
        self.api.add_resource(UserRegister, '/register')

    # 收藏接口注册
    def collect(self):
        from app.api_1.collect import CollectEt, CollectObjectEt, CollectClass, CollectOper

        self.api.add_resource(CollectEt, "/collect")  # 收藏条目
        self.api.add_resource(CollectObjectEt, "/collect/<string:c_id>")  # # 收藏单个操作API
        self.api.add_resource(CollectClass, "/collect/class")  # 收藏分类API
        self.api.add_resource(CollectOper, "/collect/oper/<string:c_id>")  # 收藏操作类

    def project(self):
        from app.api_1.project import ProjectAdmin, ProjectOper, ProjectHookToken, ProjectEventOper, ProjectCommitOper, ProjectCommit
        self.api.add_resource(ProjectAdmin, "/project")  # 项目
        self.api.add_resource(ProjectOper, "/project/<string:project_id>")  # 项目单个操作API
        self.api.add_resource(ProjectCommitOper, "/project/<string:name>/commit")  # webhook 回调
        self.api.add_resource(ProjectCommit, "/project/commit/<string:project_id>")  # 项目提交api
        self.api.add_resource(ProjectEventOper, "/project/event/<string:project_id>")  # 事件api

    def add_url(self):
        self.user()
        self.collect()
        self.project()
