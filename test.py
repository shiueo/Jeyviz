import json
import os

for user_file in os.listdir("database/users"):
    if user_file.endswith(".json"):
        with open(f"./database/users/{user_file}", 'r') as file:
            data = json.load(file)
            money = data['money']
            print(type(money))