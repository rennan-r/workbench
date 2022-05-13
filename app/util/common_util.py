import uuid
import datetime

from app.conf.app_config import AppConfig


class Common:

    @staticmethod
    def get_a_uuid():
        '''
        :return: 获取随机36位id
        '''
        return str(uuid.uuid1())

    @staticmethod
    def get_now_time():
        '''
        :return: 获取当前时间
        '''
        return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def json_result(data, func=lambda x: x):
        '''
        使用toDict处理后的对象
        :param data: sqlalchemy对象
        :param func: 自定义函数
        :return: json后对象
        '''
        return [func(i.toDict()) for i in data]

    @staticmethod
    def json_orm_result(row, data, func=lambda x: x):
        '''
        使用指定列处理的数据
        :param row: 列
        :param data: 行
        :param func: 自定义函数
        :return: json后对象
        '''
        return [func(dict(zip(row, i))) for i in data]

    @staticmethod
    def list_type(value, name):
        '''
        :param value: 参数
        :param name:  字段
        :return:
        '''
        if not value:
            return []
        elif not isinstance(value, list):
            raise ValueError(name + '参数类型错误，必须是list类型')
        return value

    @staticmethod
    def dict_type(value, name):
        '''
        :param value: 参数
        :param name:  字段
        :return:
        '''
        if not value:
            return []
        elif not isinstance(value, dict):
            raise ValueError(name + '参数类型错误，必须是dict类型')
        return value

    @staticmethod
    def json_type(value, name):
        '''
        :param value: 参数
        :param name:  字段
        :return:
        '''
        if not value:
            return []
        elif not isinstance(value, list):
            raise ValueError(name + '参数类型错误，必须是list类型')
        return value

    @staticmethod
    def github_time_format(time):
        '''
        :param time:  github时间
        :return:
        '''
        if not time:
            return ""

        return time[:-1].replace("T", " ")

    @staticmethod
    def github_hook_url(name):
        '''
        :return:
        '''
        perfix = "http://"
        format_str = "/project/{}/commit".format(name)

        return perfix + AppConfig.WUS_URL + format_str
