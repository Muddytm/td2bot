"""Script for making custom icons."""

from PIL import Image, ImageDraw, ImageFont
import json
import random
import os

template = "images/circleborder.png"


def make():
    """Make a server icon for TD2!"""
    with open("data/icons.json") as f:
        data = json.load(f)

    file = ""
    files = []
    for filename in os.listdir("images/heroes"):
        if "README" not in filename and filename not in data["used"]:
            files.append(filename)
            #full_file = "images/heroes/{}".format(filename)
            #file = filename

    if not files:
        with open("data/icons.json", "w") as f:
            data = {"used": []}
            json.dump(data, f)
        file = "arc_warden.png"
    else:
        file = random.choice(files)

    data["used"].append(file)

    img = Image.open("images/heroes/{}".format(file))
    overlay = Image.open(template)

    img.paste(overlay, (0, 0), overlay)
    img.save("images/icon.png")

    with open("data/icons.json", "w") as f:
        json.dump(data, f)

    return file.replace(".json", "")


#if __name__ == "__main__":
#    make()
