file = __file__
import os

def main_path():

    file = __file__.split(os.sep)[:-3]
    if os.name == "nt":
        file = file[1:]

    file = "c:\\"+os.path.join(*file)

    return file

