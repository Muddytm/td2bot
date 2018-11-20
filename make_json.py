import json


with open("data/hero_names.txt") as f:
    data = f.readlines()


for i in data:
    tokens = i.split("=")
    name = tokens[0].lower().strip().replace(" ", "_")
    aliases = tokens[1].strip().lower().split(", ")
    print ("{} - {}".format(name, ", ".join(aliases)))
