from easymql.core import HashComment
from easymql.datatypes.primary import PrimaryDataType
from easymql.stages import Stages


def encode(item):
    """Convert Grammar object like Integer, String etc to python type"""
    if isinstance(item, list):
        for i, value in enumerate(item):
            item[i] = encode(value)
    elif isinstance(item, dict):
        for key, value in item.items():
            item[key] = encode(value)
    elif isinstance(item, PrimaryDataType):
        item = item.value
    return item


Pipeline = Stages[1, ...]
Pipeline.ignore(HashComment())
