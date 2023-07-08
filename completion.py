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
        f"uploads/outputs//{filename}"
    )
    shutil.move(f"{filename}.zip", "uploads/outputs\\")
    return filename


def remove_config():
    os.remove("config.json")
    if os.path.exists(os.path.join(os.getcwd(), "uploads\\inputs\\userProteins.txt")):
        os.remove("uploads/inputs/userProteins.txt")
    if os.path.exists(os.path.join(os.getcwd(), "uploads\\inputs\\userPeptides.txt")):
        os.remove("uploads/inputs/userPeptides.txt")


def remove_results(filename):
    os.remove(f"uploads/outputs/{filename}")
    os.remove(f"uploads/outputs/{filename}.zip")