"""Script for making custom icons."""

from PIL import Image, ImageDraw, ImageFont
import json
import random
import os

template = "images/banner.png"


def make():
    """Make a server icon for TD2!"""
    file = ""
    with open("data/requests.json") as f:
        request_data = json.load(f)

    with open("data/icons.json") as f:
        data = json.load(f)

    if request_data:
        file = request_data[0]["hero"]
        request_data.pop(0)
        with open("data/requests.json", "w") as f:
            json.dump(request_data, f)
    else:
        files = []
        for filename in os.listdir("images/heroes"):
            if "README" not in filename and filename not in data["used"]:
                files.append(filename)
                break

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

    return file


if __name__ == "__main__":
    make()
