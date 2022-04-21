import requests

from app.conf.app_config import AppConfig


class Github:
    def __init__(self):
        self.repos = AppConfig.GITHUB_API
        self.auth = (AppConfig.GITHUB_USER, AppConfig.GITHUB_TOKEN)
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }

    def create_repository(self, name):

        json = {
            "name": name
        }
        path = "/user/repos"
        res = requests.post(url=self.repos + path, json=json, headers=self.headers,
                            auth=self.auth)
        if res.status_code == 201:
            return True, res.json()
        return False, {}

    def check_repository(self, name):

        path = "/users/{}/repos".format(AppConfig.GITHUB_USER)
        res = requests.get(url=self.repos + path, headers=self.headers,
                           auth=self.auth)
        if res.status_code == 200:
            res = res.json()
            repositories = [r["name"] for r in res]
            if name in repositories:
                return_obj = res[repositories.index(name)]
                return True, return_obj
        return False, {}

    def delete_repository(self, name):
        path = "/repos/{}/{}".format(AppConfig.GITHUB_USER, name)
        res = requests.delete(url=self.repos + path, headers=self.headers,
                              auth=self.auth)
        if res.status_code == 204:
            return True
        return False

    def lay_version(self):
        pass


github = Github()
