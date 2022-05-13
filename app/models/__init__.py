from app.conf.app_config import Configure
# flask-sqlacodegen mysql+pymysql://root:root@192.168.1.143:3306/wus --flask

def format_fields(model):
    return dict(
        [(item, getattr(model, item)) for item in model.__dict__.keys() if not item.startswith('__') and item not in Configure.blank_attr])
