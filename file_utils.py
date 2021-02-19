import json
import os


def create_dir(_dir):
    """
    Creates given directory if it is not present.
    """
    if not os.path.exists(_dir):
        os.makedirs(_dir)


def load_json(load_path):
    """
    Loads json formatted data (given as "data") from load_path
    Example inputs:
        load_path: "dirname/coco.json"
    """
    # read from path
    with open(load_path) as json_file:
        data = json.load(json_file)
    return data


def save_json(data, save_path):
    """
    Saves json formatted data (given as "data") as save_path
    Example inputs:
        data: {"image_id": 5}
        save_path: "dirname/data.json"
    """
    # create dir if not present
    save_dir = os.path.dirname(save_path)
    create_dir(save_dir)

    # export as json
    with open(save_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, separators=(",", ": "))
