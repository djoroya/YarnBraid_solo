import os 
import json
import colorama
msg = "Review the settings.json file in seetings/settings_user.py"

if os.name == "nt":
    try:
        from settings.settings_win_user import settings_win
    except:
        print(colorama.Fore.RED + "settings_win_user.py not found. See example in settings/settings_win_user.py\n" + msg)
        raise Exception("settings_win_user.py not found. See example in settings/settings_win_user.py\n" + msg)
    
def print_error(error):
    raise Exception(colorama.Fore.RED +  error + "\n" + msg)
def settings():
    path = os.path.dirname(os.path.abspath(__file__))
    # if windows
    if os.name != "nt":

        json_file = os.path.join(path,"settings_user.json")
        # comprobar que exista el archivo
        if not os.path.isfile(json_file):
            print_error("settings_user.json not found. See example in settings/settings_user.json")
            
        with open(json_file) as f:
            settings = json.load(f)

    else:
        settings = settings_win()

    #comprobar que sean path absolutos
    if not os.path.isabs(settings["lmp"]):
        print_error("lammps path must be absolute")
    if not os.path.isabs(settings["lsdyna"]):
        print_error("lsdyna path must be absolute")
    if not os.path.exists(settings["lmp"]):
        print_error("lammps path not found")
    if not os.path.exists(settings["lsdyna"]):
        print_error("lsdyna path not found")
    
    return settings