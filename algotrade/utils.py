
def from_config(config: dict, **custom_objs):
    ret = None

    class_name = config.get("class_name", None)
    if class_name and (class_name in custom_objs):
        cls = custom_objs[class_name]

        cfg = config.get("config", None)
        if cfg:
            if hasattr(cls, 'from_config'):
                ret = cls.from_config(**cfg)
            else:
                ret = cls(**cfg)
        else:
            ret = cls()

    return ret
