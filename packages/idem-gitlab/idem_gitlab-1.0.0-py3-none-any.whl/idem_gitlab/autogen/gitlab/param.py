try:
    pass

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


__func_alias__ = {"type_": "type"}


def type_(hub, value: str):
    value = value.lower()
    if "integer" in value or "number" in value:
        return "int"
    elif "float" in value:
        return "float"
    elif "json" in value:
        return "Dict[str, Any]"
    elif "array" in value:
        return "List[str]"
    elif "bool" in value:
        return "bool"
    else:
        return "str"
