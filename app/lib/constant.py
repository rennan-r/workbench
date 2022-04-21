class UserConstant:
    TOKEN_ERROR = (403, "Token Error")
    USER_PWD_ERROR = (1001, "用户名或密码错误")


class CollectConstant:
    DELETE_ET = (2001, "请先删除分类下的条目")
    REPEAT_CLASS = (2002, "分类的名称不能相同")
    REPEAT_ET = (2003, "收藏的名称不能相同")


class ProjectConstant:
    REPEAT_PROJECT = (3001, "项目名重复")
    NOT_PROJECT = (3002, "项目不存在")


defult = (0000, "请求接口错误")
