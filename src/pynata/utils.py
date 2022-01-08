import json
from datetime import datetime


def format_dict(dict_, label=None):
    indented_dict = json.dumps(dict_, indent=4)
    res = f"{label} {indented_dict}" if label else indented_dict
    return res


def prettify_date(date_str: str):
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date.strftime("%Y-%m-%d %H:%M:%S")
