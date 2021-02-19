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


def list_files(
    directory: str,
    contains: list = [".json"],
    verbose: int = 1,
) -> list:
    """
    Walk given directory and return a list of file path with desired extension
    Args:
        directory: str
            "data/coco/"
        contains: list
            A list of strings to check if the target file contains them, example: ["coco.png", ".jpg", "jpeg"]
        verbose: int
            0: no print
            1: print number of files
    Returns:
        filepath_list : list
            List of file paths
    """
    # define verboseprint
    verboseprint = print if verbose else lambda *a, **k: None

    filepath_list = []

    for file in os.listdir(directory):
        # check if filename contains any of the terms given in contains list
        if any(strtocheck in file for strtocheck in contains):
            filepath = os.path.join(directory, file)
            filepath_list.append(filepath)

    number_of_files = len(filepath_list)
    folder_name = directory.split(os.sep)[-1]

    verboseprint(
        "There are {} listed files in folder {}.".format(number_of_files, folder_name)
    )

    return filepath_list
