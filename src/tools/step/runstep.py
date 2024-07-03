
import os
from tools.basic.createFolder     import createFolder
from tools.basic.loadsavejson     import savejson
from settings.settings import settings
import time
import traceback
import colorama
import datetime
settings = settings()

error_msg = {0:"Correct Execution",
             1:"Something went wrong"}

def runstep(func):
    def wa(*args, **kwargs):
        # take params
        params        = args[0]
        output_folder = args[1]
        # Create the output folder
        #output_folder = os.path.abspath(output_folder)
        params["output_folder"] = output_folder
        
        createFolder(output_folder)
        # save params in init.json
        json_path = os.path.join(output_folder,"init.json")
        savejson(params,json_path)
        # add settings
        params["init_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for ikey in settings.keys():
            params[ikey] = settings[ikey]
        # Execute the function
        t = time.time()
        current_folder = os.getcwd()
        try:
            func(*args, **kwargs)
            err = 0
        except Exception as e:
            os.chdir(current_folder)
            print(colorama.Fore.RED + "Error in step: " + func.__name__)
            traceback.print_exc()
            print(colorama.Fore.RESET) 
            # save the error in error.log in output_folder
            error_log = os.path.join(output_folder,"error.log")
            with open(error_log,"w") as f:
                f.write(traceback.format_exc())
            raise Exception(e)
            err = 1
        os.chdir(current_folder)

        # Compute the elapsed time
        elapsed = time.time() - t
        # remove settings
        for ikey in settings.keys():
            del params[ikey]
        # Save the params
        params["error"]     = err
        params["error_msg"] = error_msg[err]
        params["elapsed"] = elapsed
        params["final_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params["root_folder"] = os.path.abspath(output_folder).replace(output_folder,"")
        json_path = os.path.join(output_folder,"params.json")

        savejson(params,json_path)

        # info.json
        params_info = dict()
        params_info["elapsed"] = elapsed
        params_info["error"] = err
        params_info["final_time"] = params["final_time"] 
        # if key comment exists, add it
        if "comment" in params.keys():
            params_info["comment"] = params["comment"]

        json_path = os.path.join(output_folder,"info.json")
        savejson(params_info,json_path)
    return wa