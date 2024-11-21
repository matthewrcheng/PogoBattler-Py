import json

with open('effectiveness.json') as f:
    effectiveness = json.load(f)

with open('gamemaster.json') as f:
    settings = json.load(f).get("settings")