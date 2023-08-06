import json


def read_json(filepath):
    """
    Reads a json file, and returns the data
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def write_json(filepath, data):
    """
    Writes a json file with the given data, or creates one if it doesn't exist
    """
    with open(filepath, "w") as f:
        json.dump(data, f)


def get_json_key(filepath, keyname):
    """
    Gets a json file key
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return data[keyname]


def get_key(filepath, keyname):
    """
    An alias for -
    ```py
    fileops.jsonops.get_json_key()
    ```
    """
    return get_json_key(filepath, keyname)
