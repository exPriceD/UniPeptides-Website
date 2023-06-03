import os
import shutil
import json


def creating_zip():
    with open("config.json", "r") as json_cfg:
        config = json.load(json_cfg)
    base = os.path.basename(config["savePath"]["value"])
    filename = os.path.splitext(base)[0]
    shutil.make_archive(
        filename,
        'zip',
        f"C:\\Users\\loler\\PycharmProjects\\UniPeptides-website\\output\\{filename}"
    )
    shutil.move(f"{filename}.zip", "C:\\Users\\loler\\PycharmProjects\\UniPeptides-website\\output\\")
    return filename


def remove_user_config():
    os.remove("config.json")