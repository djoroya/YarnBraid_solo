import colorama
import os
import pandas as pd
def pprint(params_lmp,tabs=""):

    try:
        error = params_lmp["error"]
        error = error if error else False
    except:
        error = 0



    
    for ikey in params_lmp:
        if ikey == "cmd":
            continue
        # if ikey is a numpy matrix, show the shape
        if params_lmp[ikey].__class__.__name__ == "ndarray":
            msg = "np array with shape"+ params_lmp[ikey].shape.__str__()
        # if path
        elif params_lmp[ikey].__class__.__name__ == "str" and os.path.exists(params_lmp[ikey]):
            # detect if is a file or a folder
            string = params_lmp[ikey]

            if os.path.isfile(params_lmp[ikey]):
                string = string.split("/")[-2:]
            else:
                string = string.split("/")[-3:]

            msg = "/".join(string)
        elif ikey == "cmd":
            # split the command in lines by ;
            msg = params_lmp[ikey].split(";")
            msg = "\n\t-".join(msg)
            msg = "\n\t- " + msg
        elif type(params_lmp[ikey]) == dict:
            # only show the keys
            msg = list(params_lmp[ikey].keys())
            # show 10 keys and ...
            msg = msg[:10] + ["..."]
            msg = "\n\t-".join(msg)
            msg = "\n\t- " + msg
        elif ikey == "elapsed":
            time = params_lmp[ikey]
            # convert time to hours minutes and seconds
            seconds = time % 60
            minutes = (time//60) % 60
            hours   = (time//60)//60
            # round 
            seconds = round(seconds,2)
            minutes = int(minutes)
            hours   = int(hours)
            msg = "{} h  -  {} m  -  {} s".format(hours,minutes,seconds)
        elif type(params_lmp[ikey]) == pd.DataFrame:
            # only show the keys
            msg = list(params_lmp[ikey].keys())
            # show Pandas DataFrame with shape
            msg = "Pandas DataFrame with shape "+params_lmp[ikey].shape.__str__()
        
        else:
            msg = params_lmp[ikey]
        # complete key to have 15 characters
        ikey_str = ikey + " "*(20-len(ikey))

        if (ikey == "error" or ikey == "error_msg"):
            if error:
                print(tabs+colorama.Fore.RED  + ikey_str +\
                      colorama.Fore.RED  +   ":", msg)
            else:
                print(tabs+colorama.Fore.GREEN+ ikey_str +\
                      colorama.Fore.GREEN+   ":", msg)
        
        else:
            print(tabs+colorama.Fore.BLUE + ikey_str +\
                  colorama.Fore.RESET + ":", msg)