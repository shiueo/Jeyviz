import json


def json_dump(data, path):
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, indent="\t", ensure_ascii=False)


def json_open(path):
    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)
        return data
