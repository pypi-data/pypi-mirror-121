import re
import copy
from typing import TypeVar

regex_camel_case = r'[a-z]+[a-z0-9]*[A-Z][A-Za-z0-9]*'

def is_camel_case(name: str) -> bool:
    return re.fullmatch(regex_camel_case, name) is not None
    
def to_snake_case(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

def is_snakable(obj: object) -> bool:
    set_attr = set(dir(obj))

    duplicated_attr_name = [attr_name for attr_name in dir(obj) if is_camel_case(attr_name) and to_snake_case(attr_name) in set_attr]

    return False if duplicated_attr_name else True

class Converter:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        setattr(obj, self.name, value)

T = TypeVar('T')
def snake(obj: T) -> T:
    if not is_snakable(obj):
        raise Exception('This object is not snakable!')

    obj = copy.copy(obj)

    camel_class_vars = [(name, value) for name, value in vars(obj.__class__).items() if is_camel_case(name)]
    for name, value in camel_class_vars:
        setattr(obj.__class__, to_snake_case(name), Converter(name))

    camel_vars = [(name, value) for name, value in vars(obj).items() if is_camel_case(name)]
    for name, value in camel_vars:
        setattr(obj.__class__, to_snake_case(name), Converter(name))

    return obj