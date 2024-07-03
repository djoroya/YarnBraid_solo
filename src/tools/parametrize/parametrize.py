
import numpy as np
import pandas as pd
from tools.basic.loadsavejson import  savejson
from tools.basic.path_gen import path_gen
import os
import time
from tools.parametrize.html import mostrar_tabla,dataframize,setvalue,init_table
import traceback
class cont():
    def __init__(self,fcn):
        self.i = 0
        self.fcn = fcn
        self.nsteps = 20
    def run(self,nstep=None):
        if nstep is None:
            self.i += 1
            self.fcn(self.i)
        else:    
            self.nsteps = nstep


def parametrize(main_path,Run,vars,default):

    # main_path is the path where the vars.json will be saved
    # Run is a function that runs the simulation. It must have two arguments:
    # -params: a dictionary with the parameters
    # -output_folder: the path where the simulation will be run
    # vars is a dictionary with the variables to parametrize
    # default is a function that returns a dictionary with the default values
    
    df = dataframize(vars)

    json = { "vars" : vars,
             "df"   : df   ,
             "paths": []   ,
             "main_path": main_path,
             "main_path_abs": os.path.abspath(main_path),
             "finished": False  }
    json_path = os.path.join(main_path,"vars.json")
    savejson(json, json_path)

    procesos = [ "Exp-"+str(i+1) for i in df.index.values]
    procesos = init_table(vars,procesos,df)


    # format vars columns .4e
    for ivar in vars.keys():
        procesos[ivar] = procesos[ivar].astype(type(vars[ivar]["span"][0]))
        if type(vars[ivar]["span"][0]) != str:
            # if not int
            if type(vars[ivar]["span"][0]) != int:
                procesos[ivar] = procesos[ivar].map(lambda x: "{:.2e}".format(x))


    all_params = []
    callback = dict()
    nsteps_list = []
    times = [0]
    for i in range(len(df)):
        params = default()
        loop_path = os.path.join(main_path,path_gen())

        json["paths"].append(loop_path)
        savejson(json, json_path)

        t = time.time()
        c = cont(None)
        c.fcn    = lambda j: mostrar_tabla(procesos,i,j-1,c.nsteps,times)
        callback = c.run
        error = False

        for ivar in vars.keys():
            setvalue(params,vars[ivar]["path"],df[ivar][i])
        # 
        current_path = os.getcwd()
        try:
            params = Run(params,loop_path,callback=callback)
        except Exception as e:
            os.chdir(current_path)
            error = True
            print("Error in Run function")
            # save error message in txt file
            name = os.path.join(loop_path,"error_{:d}.txt".format(i))
            try:
                with open(name,"w") as f:
                    f.write(traceback.format_exc())
            except:
                print("Error saving error message")

        nsteps_list.append(c.i)
        t = time.time() - t
        procesos["time"][i] = "{:.2f}".format(t)

        procesos["Status"][i] = "✅" if not error else "❌"        
        if not error:
            mostrar_tabla(procesos,i,c.nsteps-1,c.nsteps,times)
        else:
            mostrar_tabla(procesos,i,c.i-1,c.nsteps,times)

        all_params.append(params)
        times.append(t)

    json["finished"] = True
    savejson(json, json_path)
