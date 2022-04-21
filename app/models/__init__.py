from app.conf.app_config import Configure


def format_fields(model):
    return dict(
        [(item, getattr(model, item)) for item in model.__dict__.keys() if not item.startswith('__') and item not in Configure.blank_attr])
