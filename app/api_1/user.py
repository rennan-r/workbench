from flask_restful import Resource

from app.api_1 import args_parse
from app.api_1.mysql_common.api_common import APIResource
from app.lib.APIException import ApiException
from app.lib.Wus_Response import return_response, return_error
from app.models.user_model import User
from app.util.common_util import Common
from app.util.encryption_util import Encryption
from app.api_1.mysql_common.user_common import UserCommon
from app.conf.app_config import Configure
from app.lib.constant import UserConstant


# 登录
class UserLogin(APIResource):
    model = User

    @args_parse(schemy={
        "username": {"type": str, "required": True},
        "password": {"type": str, "required": True}
    })
    def post(self, username, password):
        user = self.get_one(User.username, username)
        if not user or user.password != Encryption.md5_encryption(password):
            # 用户存在或者用户名密码错误
            raise ApiException(*UserConstant.USER_PWD_ERROR)
        data = {
            "token": Encryption.jwt_encode({
                "u_id": user.u_id
            }),
            "user": {
                "username": user.username,
            },
            "expireAt": 1 / 8
        }
        return return_response(data=data, message="登录成功")


# 注册
class UserRegister(APIResource):
    model = User

    @args_parse(schemy={
        "username": {"type": str, "required": True, "trim": True},
        "password": {"type": str, "required": True, "trim": True}
    })
    def post(self, username, password):
        lens = len(password)
        if Configure.password_length[0] <= lens <= Configure.password_length[1]:
            self.increase_one(u_id=Common.get_a_uuid(), username=username,
                              password=Encryption.md5_encryption(password),
                              create_time=Common.get_now_time(),
                              approve=0)

        return return_response(data={"username": username})
