import os
from tools.step.runstep           import runstep,lj,address
import numpy as np

from models.direct.InflationDirect.functions.LoadInp import LoadInp
from models.direct.InflationDirect.functions.addStep import addStep


from tools.calculix.runccx import runccx
from tools.search_contacts              import search_contacts
join = os.path.join

@runstep(address(__file__))
def RunInflationDirect(params,out_folder):

    gmsh_params    = lj(params["gmsh_path"])
    lammps_params  = lj(gmsh_params["lammps_path"])
    out_folder     = params["output_folder"]
    
    young    = 2960 # Este es el modulo de young del material que se usa en la inflacion
    lamb     = gmsh_params["factor_radius"]
    if params["auto_pressure"]:
        params["pressure"] = young * (1-lamb)/lamb

    params["lammps_params"] = lammps_params
    params["gmsh_params"]   = gmsh_params
    #
    lamb = gmsh_params["factor_radius"]
    young    = 2960 # Este es el modulo de young del material que se usa en la inflacion

    params["pressure"] = young * (1-lamb)/lamb

    df = gmsh_params["trajs"]
    # change xu yu zu -> x,y,z columns names
    df.columns = ["type","x","y","z"]

    
    df = [ df[df["type"]==i][["x","y","z"]].values 
          for i in np.unique(df["type"]) ]
    df = [ df[i] for i in range(len(df))]

    # factor length gmsh_params["factor_length"]

    # Necesitamos agregar muchos puntos para que al buscar
    
    # puntos cercanos a las curvas no se pierdan puntos
    # df = df_respan(df)
    params["h"] = lammps_params["h"]
    params["all_bonds"] = lammps_params["all_bonds"]
    inp_file = LoadInp(gmsh_params,df,params)

    # inp_file.SetUniqueNodes()
    file = os.path.join(out_folder,"init.inp")

    inp_file.print(file)

    radius = lammps_params["r_hebra"]
    contacts = search_contacts(df,th = 4*radius)

    if params["ties_activate"]:
        ties = []
        for i in np.arange(0,64,4):
            for k in range(3):
                ties.append([i+k+1,i+k+2])
                print(i+k+1,i+k+2)

        # save the contacts

        contacts_set = {tuple(contact) for contact in contacts}
        ties_set = {tuple(tie) for tie in ties}

        # Eliminamos los pares que aparecen en ties de contacts usando diferencia de conjuntos
        filtered_contacts_set = contacts_set - ties_set

        # Convertimos el resultado de nuevo a lista para mostrar
        filtered_contacts_set = list(filtered_contacts_set)
        filtered_contacts_set.sort()
        #tuples to list
        filtered_contacts = [list(contact) for contact in filtered_contacts_set]

        contacts = filtered_contacts

        params["ties"] = np.array(ties)

        
    params["contacts"] = np.array(contacts)

    addStep(inp_file,contacts,file,params)

    name_nsets = [ inset.name     for inset in inp_file.nsets]
    data_nsets = [ inset.id_nodes for inset in inp_file.nsets]

    nset_dict = dict(zip(name_nsets,data_nsets))

    params["nsets"] = nset_dict

    params["r_hebra"] = lammps_params["r_hebra"]

    runccx(out_folder, "init",mpi=params["mpi"],
           mpi_np=params["mpi_np"],
           OMP_NUM_THREADS=params["OMP_NUM_THREADS"],
           dynamic=params["calculix_dynamic"])  