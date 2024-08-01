import json
import pandas as pd 

with open("imdb250.json", "r", encoding="UTF-8") as file:
    data = json.load(file)

print(data)