

class DictObjHelper:
    @staticmethod
    def check_value(dict_obj, element_name):
        return dict_obj is not None and element_name in dict_obj

    @staticmethod
    def get_value(dict_obj, element_name, default_value):
        if dict_obj is None or element_name not in dict_obj:
            return default_value
        try:
            _value = dict_obj[element_name]
            _type = type(default_value)
            if _type is bool:
                return bool(_value)
            if _type is int:
                return int(_value)
            if _type is float:
                return float(_value)
            if _type is complex:
                return complex(_value)
            if _type is str:
                return str(_value)
            if _type is list:
                return list(_value)
            if _type is tuple:
                return tuple(_value)
            if _type is set:
                return set(_value)
            if _type is dict:
                return dict(_value)
            return _value
        except:
            return default_value

