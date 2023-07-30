import datetime
import os

from essentials.json_util import json_dump


def send_mail(path, title, content, sender, receiver_id, image=""):
    json_path = f"{path}/database/mails/{receiver_id}/{len(os.listdir(f'{path}/database/mails/{receiver_id}'))}.json"
    print(json_path)

    data = {
        "title": title,
        "content": content,
        "from": sender.name,
        "date": datetime.datetime.today().strftime("%m/%d/%Y %H:%M:%S"),
        "image": image,
    }

    json_dump(data, json_path)
