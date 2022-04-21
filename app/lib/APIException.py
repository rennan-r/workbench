from app.lib.Wus_Response import return_error


class ApiException(Exception):
    code = 0000

    def __init__(self, code, msg):

        self.code = code
        self.msg = msg

    def to_dict(self):
        return return_error(self.code, self.msg)




