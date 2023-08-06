import os
import subprocess


def get_data_path(*path):
    current_folder = os.path.dirname(__file__)
    return os.path.join(current_folder, "data", *path)


def get_data(*path: str):
    path = get_data_path(*path)
    with open(path) as f:
        data = f.read()
    return data


def run(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
