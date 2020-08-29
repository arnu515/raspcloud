import json
import os
from .. import check_config


check_config()
CONFIG_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../config.json"


def get_config(key: str):
    check_config()
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        return config.get(key)


def set_config(key: str, value):
    check_config()
    with open(CONFIG_PATH, "r+") as f:
        x = json.load(f)
        x[key] = value
        f.seek(0, 0)
        f.truncate(0)
        json.dump(x, f, indent=4)
