file = __file__
import os

def simulations():

    file = __file__.split(os.sep)[:-3]
    if os.name == "nt":
        file = file[1:]

    file = "c:\\"+os.path.join(*file,"simulations")

    return file

def simulations_list():
    path_list =  simulations().split(os.sep)
    if os.name == "nt":
        path_list = path_list[1:]
    return path_list