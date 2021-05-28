import json


def get_params():
    with open('short.json','r',encoding='utf-8') as f:
        data = json.load(f)
    if len(data) < 1:
        data = {}
    return data