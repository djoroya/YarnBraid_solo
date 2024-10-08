import os
from tools.step.runstep           import runstep
from tools.basic.loadsavejson     import loadjson

from model.inflation.table.LoadInp   import LoadInp
from model.inflation.df_respan import df_respan

from model.inflation.table.addStep          import addStep
import numpy as np
from tools.calculix.runccx import runccx
from tools.search_contacts              import search_contacts
from settings.simulations import simulations
join = os.path.join
lj   = lambda *x: loadjson(join(simulations(),*x, "params.json"))

@runstep("RunInflation")
def RunInflation(params,out_folder):

    gmsh_params    = lj(params["gmsh_path"])
    lammps_params  = lj(gmsh_params["lammps_path"])
    out_folder     = params["output_folder"]
    
    params["lammps_params"] = lammps_params
    params["gmsh_params"]   = gmsh_params
    #
    lamb = gmsh_params["factor_radius"]
    young    = 2960 # Este es el modulo de young del material que se usa en la inflacion

    params["pressure"] = young * (1-lamb)/lamb

    df = lammps_params["old_df"]
    # change xu yu zu -> x,y,z columns names
    df.columns = ["type","x","y","z"]

    
    df = [ df[df["type"]==i] for i in np.unique(df["type"]) ]
    # Necesitamos agregar muchos puntos para que al buscar
    
    # puntos cercanos a las curvas no se pierdan puntos
    # df = df_respan(df)

    inp_file = LoadInp(gmsh_params,df,params)

    # inp_file.SetUniqueNodes()
    file = os.path.join(out_folder,"init.inp")

    inp_file.print(file)

    radius = lammps_params["r_hebra"]
    contacts = search_contacts(df,th = 6*radius)
    # save the contacts
    params["contacts"] = contacts

    addStep(inp_file,contacts,file,params)

    runccx(out_folder, "init",mpi=params["mpi"],
           mpi_np=params["mpi_np"],
           OMP_NUM_THREADS=params["OMP_NUM_THREADS"],
           dynamic=params["calculix_dynamic"])  