from utils import query
import json
with open("./utils/dict_logo.json") as json_file:
    data = json.load(json_file)

print(query.query_img("test2.PNG", data))