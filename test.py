from essentials.json_util import json_dump

data = {
	"title": "해봐",
	"content": "json읽기 힘들죠? 못읽겠죠?",
	"from": "shiueo",
	"date": "07/31/2023 04:40:46",
	"image": "https://pbs.twimg.com/media/F1Gqg8UX0AE1a_x?format=jpg&name=4096x4096"
}



for i in range(2001, 65537):
    json_dump(data, f"./dummy/{i}.json")
	print(i)