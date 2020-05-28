def from_config(config: dict, **custom_objs):
    ret = None

    class_name = config.get("class_name", None)
    if class_name and (class_name in custom_objs):
        ret = custom_objs[class_name]

        cfg = config.get("config", None)
        if cfg and hasattr(ret, 'from_config'):
            ret = ret.from_config(**cfg)
        else:
            ret = ret()

    return ret
