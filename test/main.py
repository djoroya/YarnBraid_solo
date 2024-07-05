import glob,os
import importlib
import sys
from tools.basic.loadsavejson import savejson

# remove all log files
log_files = glob.glob("log/*.log")
for ilog in log_files:
    os.remove(ilog)
    


tests = glob.glob('tests/**/*.py')
modules = [ itest.replace(os.sep,".").replace(".py","") for itest in tests]
name_fcn = [ imod.split(".")[-1] for imod in modules ]

main_log = "main.log"
main_log_file = open("log/"+main_log,"w")

results = []
for i in range(len(modules)):

    sys.stdout = main_log_file

    print("module: ",modules[i])
    print("name_fcn: ",name_fcn[i])
    module = importlib.import_module(modules[i])
    fcn = getattr(module,name_fcn[i])

    log_file = open("log/"+name_fcn[i]+".log","w")
    sys.stdout = log_file

    print("running test: ",name_fcn[i])
    error = False
    try:
        fcn()
    except Exception as e:
        error = True
        print("error: ",e)
        print("test ",name_fcn[i]," failed")

    log_file.close()

    results.append({
        "name_fcn":name_fcn[i],
        "error": error
    })
    
    # change stdout back to console
    sys.stdout = main_log_file

    print("test ",name_fcn[i]," done")

sys.stdout = sys.__stdout__

main_log_file.close()

savejson({"results:":results},"log/results.json")
