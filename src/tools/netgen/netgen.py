import meshio
from tools.calculix.inp.inp import inp
import os
from settings.settings import settings
from tools.step.runstep import runstep
from tools.calculix.inp.inp import inp 
import subprocess

settings = settings()
NetGen = settings["netgen"]

# folder 
folder = __file__.split("netgen.py")[0]
lines = open(os.path.join(folder,"meshParameters"), "r").readlines()
lines_gp = [ lines[i:i+2] for i in range(0, len(lines), 2) ]
lines_dict = [  {ilin[0].split()[1]:ilin[0].split()[0] }
            for ilin in lines_gp ]

lines_value = [ lines[i:i+2] for i in range(1, len(lines), 2) ]
lines_value = [ iline[0].replace("\n","") for iline in lines_value ]
type_dict = { list(idict.keys())[0]:list(idict.values())[0] 
                for idict in lines_dict }


def default_params_netgen():
    
    default_dict = { list(idict.keys())[0]:iline
                    for idict, iline in zip(lines_dict, lines_value) }

    default_dict = { "netgen_params":default_dict ,
                    "factor_min":0.9,
                    "factor_max":1.1,
                    "verbose":False}
    return default_dict

# function to write the meshParameters file
def write_meshParameters(meshParameter,file_path):
    with open(file_path, "w") as f:
        for key, value in meshParameter.items():
            f.write(type_dict[key] + "   "+str(key) + " \n" + str(value) + "\n")

def runsys(command):

    #if os.name == "nt":
    command = command.split()
    error_stdout = open("error.txt", 'wb')
    outpt_stdout = open("out.txt", 'wb')
    subprocess.run(command, 
    stdout=outpt_stdout, 
    stderr=error_stdout, 
    shell=False)
    # else:
    #os.system(command)
@runstep
def RunNetGen(params,output_folder):

    cur = os.getcwd()
    os.chdir(output_folder)
    # ==========
    step_file = params["step_file"]
    # 
    #step_file = os.path.abspath(step_file)
    runsys(NetGen + " STEP_ASSEMBLY_SPLIT_TO_COMPOUNDS " + step_file + " out.brep") 
    runsys(NetGen + " BREP_COMPOUND out_solid_0001.brep out_solid_0002.brep out_solid_0003.brep geometry.brep")
    # create meshRefinement file "0\n\0"
    with open("meshRefinement", "w") as f:
        f.write("0\n0\n")

    # remove step_file from params
    write_meshParameters(params["netgen_params"],"meshParameters")

    runsys(NetGen + " BREP_MESH geometry.brep out.vol meshParameters meshRefinement")
    mesh = meshio.read("out.vol")

    # C3D10MH is not supported by CalculiX
    meshio.write("out.inp", mesh, file_format="abaqus")

    inp_f = inp("out.inp",warning=False)
    inp_f.print("out_processed.inp")

    os.chdir(cur)

    inp_file = os.path.join(params["output_folder"],"out.inp")

    inp_f = inp(inp_file,warning=False)

    out_file = os.path.join(params["output_folder"],"out_re.inp")
    inp_f.print(out_file)


@runstep
def RunNetGenFull(params,output_folder):

    cur = os.getcwd()
    os.chdir(output_folder)
    # ==========
    step_file = params["step_file"]
    # 
    #step_file = os.path.abspath(step_file)
    runsys(NetGen + " STEP_ASSEMBLY_SPLIT_TO_COMPOUNDS " +\
            step_file + " out.brep") 
    # create meshRefinement file "0\n\0"
    with open("meshRefinement", "w") as f:
        f.write("0\n0\n")

    # remove step_file from params
    write_meshParameters(params["netgen_params"],"meshParameters")

    runsys(NetGen + " BREP_MESH out_solid_0001.brep out.vol meshParameters meshRefinement")
    mesh = meshio.read("out.vol")

    # C3D10MH is not supported by CalculiX
    meshio.write("out.inp", mesh, file_format="abaqus")

    inp_f = inp("out.inp",warning=False)
    inp_f.print("out_processed.inp")

    os.chdir(cur)

    inp_file = os.path.join(params["output_folder"],"out.inp")

    inp_f = inp(inp_file,warning=False)

    out_file = os.path.join(params["output_folder"],"out_re.inp")
    inp_f.print(out_file)