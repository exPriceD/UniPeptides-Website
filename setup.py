import json
import re
import os
import datetime


def creatingLogs():
    logs = {
        "missing": {
            "proteins": []
        },
        "siteProblems": False,
        "unexpectedError": False
    }

    with open("errorLogs.json", "w") as errorLogs:
        json.dump(logs, errorLogs, indent=4)


def setupConfig():
    if not os.path.isdir('output'):
        os.mkdir("output")

    time = str(datetime.datetime.today().replace(microsecond=0)).replace(':', ' ').replace(' ', '')
    mk_name = f"Result{time}"
    os.mkdir(f"output/{mk_name}")

    config = {
        "proteins": {
            "value": []
        },
        "peptides": {
            "value": []
        },
        "savePath": {
            "value": f"C:\\Users\\loler\\PycharmProjects\\UniPeptides-website\\output\\{mk_name}"
        },
        "databasePath": {
            "value": ''
        },
        "proteinsPath": {
            "value": ''
        },
        "excelFilters": {
            "entryIdentifier": True,
            "entryName": False,
            "entryType": False,
            "fullName": False,
            "scientificName": False,
            "commonName": False,
            "genes": False,
            "proteinExistence": False,
            "length": False,
            "massDa": False,
            "category": False,
            "id": False,
            "sequence": False,
            "sequence_length": False,
            "occurrence": False,
            "relative": False,
            "position": False,
            "nter": False,
            "cter": False
        }
    }

    with open("config.json", "w") as json_cfg:
        json.dump(config, json_cfg, indent=4)


def filling_config(user_data: dict):
    with open("config.json", "r") as json_cfg:
        config = json.load(json_cfg)

    for key in user_data.keys():
        if key == "proteins_value":
            config["proteins"]["value"].extend(filter(None, re.split('[;, .]+', user_data[key])))
            continue
        if key == "peptides_value":
            config["peptides"]["value"].extend(filter(None, re.split('[;, .]+', user_data[key])))
            continue
        config["excelFilters"][key] = True if user_data[key] == "true" else False

    with open("config.json", "w") as json_cfg:
        json.dump(config, json_cfg, indent=4)


def saveFilters():
    with open("config.json", "r") as json_cfg:
        config_data = json.load(json_cfg)
        config_data["proteins"]["value"] = []
        config_data["peptides"]["value"] = []
        config_data["savePath"]["value"] = ''
        config_data["databasePath"]["value"] = ''
        config_data["proteinsPath"]["value"] = ''
    with open("config.json", "w") as json_cfg:
        json.dump(config_data, json_cfg, indent=4)
