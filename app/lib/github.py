import requests

from app.conf.app_config import AppConfig
from app.util.common_util import Common


class Github:
    def __init__(self):
        self.repos = AppConfig.GITHUB_API
        self.auth = (AppConfig.GITHUB_USER, AppConfig.GITHUB_TOKEN)
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }

        self.success = lambda res: True
        self.fail = lambda res: False
        self.fail2 = lambda res: False, {}

    def request(self, path, status_code, success, fail, method="get", json={}):
        res = getattr(requests, method)(url=self.repos + path, json=json, headers=self.headers,
                                        auth=self.auth)

        if res.status_code == status_code:
            return success(res)
        return fail(res)

    def create_repository(self, name):

        json = {
            "name": name
        }
        path, success= "/user/repos", lambda res: (True, res.json())

        return self.request(path=path, method="post", status_code=201, success=success, fail=self.fail2, json=json)

    def check_repository(self, name):

        path = "/users/{}/repos".format(AppConfig.GITHUB_USER)

        def success(res):
            res = res.json()
            repositories = [r["name"] for r in res]
            if name in repositories:
                return_obj = res[repositories.index(name)]
                return True, return_obj

            return False, {}

        return self.request(path=path, method="get", status_code=200, success=success, fail=self.fail2)

    def delete_repository(self, name):
        path = "/repos/{}/{}".format(AppConfig.GITHUB_USER, name)

        return self.request(path=path, method="delete", status_code=204, success=self.success, fail=self.fail)

    def lay_version(self, project_id, name):
        path = "/repos/{}/{}/commits".format(AppConfig.GITHUB_USER, name)

        def success(res):
            commits = []
            for commit in res.json():
                c = commit["commit"]["author"]
                message = commit["commit"]["message"]
                dic = {
                    "author": c["name"],
                    "message": message,
                    "commit_time": Common.github_time_format(c["date"]),
                    "email": c["email"],
                }
                commits.append(dic)
            return commits

        res = self.request(path=path, method="get", status_code=200, success=success, fail=self.fail)
        if not res:
            return []
        for commit in res:
            commit["id"] = Common.get_a_uuid()
            commit["project_id"] = project_id
        return res


github = Github()
