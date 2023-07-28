import datetime
import os
import random
import hashlib

from essentials.json_util import json_dump
from essentials.residential import create_house


def create_user(path, config, logger, author_id, author_name):
    json_path = f"{path}/database/users/{author_id}.json"

    chosen_region = random.choice(config["regions"])
    chosen_house_type = random.choice(config["residential_types"])

    if not os.path.isdir(f"{path}/database/residential/{author_id}"):
        os.mkdir(f"{path}/database/residential/{author_id}")

    house_name = hashlib.md5(
        str(
            (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
        ).encode()
    ).hexdigest()

    create_house(path, config, chosen_region, author_id, house_name, chosen_house_type)

    data = {
        "manager": 0,
        "noble": 0,
        "money": 6000000,
        "owned_company": [],
        "employed_company": [],
        "primary_house": house_name,
        "happiness": random.randint(50, 100),
        "health": random.randint(50, 100),
    }

    json_dump(data, json_path)

    logger.info(
        f"New User {author_name} Joined! - {chosen_region} - {chosen_house_type}"
    )
    return chosen_region
