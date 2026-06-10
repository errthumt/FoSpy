import os
import importlib.resources as pkg_resources

def get_default_file():
    return pkg_resources.files(__package__).joinpath("defaults.json")

def get_user_file():
    file = pkg_resources.files(__package__).joinpath("user.json")
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("{}")
    return file

def get_enforced_file():
    file = pkg_resources.files(__package__).joinpath("enforced.json")
    return file