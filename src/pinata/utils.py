import json


def format_dict(dict_, label=None):
    indented_dict = json.dumps(dict_, indent=4)
    res = f"{label} {indented_dict}" if label else indented_dict
    return res
