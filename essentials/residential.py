import os
import random

from essentials.functions import house_cost_function
from essentials.json_util import json_open, json_dump


def create_house(path, config, region, author_id, house_name, house_type):
    house_json_path = f"{path}/database/residential/{author_id}/{house_name}.json"

    region_data = json_open(f"{path}/database/regions/{region}.json")

    region_state = region_data["parent"]
    state_data = json_open(f"{path}/database/states/{region_state}.json")

    house_data = {
        "owner": author_id,
        "name": house_name,
        "region": region,
        "house_type": house_type,
        "cost": house_cost_function(
            minimum_cost=state_data[f"{house_type}_min"],
            inflation=state_data["inflation"],
        ),
    }
    region_data["residential"] += state_data[f"{house_type}_residential_score"]

    json_dump(house_data, house_json_path)
    json_dump(region_data, f"{path}/database/regions/{region}.json")


def delete_house(path, config, author_id, house_name):
    house_json_path = f"{path}/database/residential/{author_id}/{house_name}.json"
    house_data = json_open(house_json_path)

    region = house_data['region']
    region_data = json_open(f"{path}/database/regions/{region}.json")

    region_state = region_data["parent"]
    state_data = json_open(f"{path}/database/states/{region_state}.json")

    region_data["residential"] -= state_data[f"{house_data['house_type']}_residential_score"]

    os.remove(house_json_path)
    json_dump(region_data, f"{path}/database/regions/{region}.json")


def edit_house_name(path, author_id, old_name, target_house_path, new_name):
    user_data = json_open(f"{path}/database/users/{author_id}.json")
    if user_data["primary_house"] == old_name:
        user_data["primary_house"] = new_name
        json_dump(user_data, f"{path}/database/users/{author_id}.json")
    house_data = json_open(target_house_path)
    house_data["name"] = new_name
    os.remove(target_house_path)
    json_dump(house_data, f"{path}/database/residential/{author_id}/{new_name}.json")
    return house_data["region"], house_data["house_type"]


def edit_house_cost(target_house_path, new_cost):
    house_data = json_open(target_house_path)
    old_cost = house_data["cost"]
    house_data["cost"] = new_cost
    json_dump(house_data, target_house_path)
    return house_data["region"], house_data["house_type"], old_cost
