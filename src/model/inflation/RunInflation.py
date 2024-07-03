

from model.inflation.df_respan         import df_respan
from model.inflation.LoadInp           import LoadInp
from model.inflation.addStep           import addStep
from model.inflation.ComputeRadius     import ComputeRadius
from model.inflation.ComputeDenier     import ComputeDenier
from model.inflation.CreateDeformedInp import CreateDeformedInp
import os
from tools.basic.loadsavejson           import loadjson,savejson
from tools.step.runstep                 import runstep
from tools.search_contacts              import search_contacts
from tools.calculix.inp.addSurfaceGen   import addSurface
from tools.calculix.runccx              import runccx
import pandas as pd
import numpy  as np

@runstep
def RunInflation(params,output_folder):

    output_folder = params["output_folder"]

    json_path_file = os.path.join(params["gmsh_path"], "params.json")
    gmsh_params   = loadjson(json_path_file)

    json_path_file = os.path.join(gmsh_params["root_folder"],
                                  gmsh_params["lsdyna_path"], 
                                  "params.json")
    lsdyna_params = loadjson(json_path_file)

    json_path_file = os.path.join(lsdyna_params["root_folder"],
                                  lsdyna_params["lmp_path"], 
                                  "params.json")

    lmp_params     = loadjson(json_path_file)

    nhilos = lmp_params["nhilos"]
    params["theta"] = lmp_params["theta"]
    
    df = df_respan(lsdyna_params,nhilos)
    # Load the inp files and create the inp class for each one
    # and create a nset of faces
    inp_files = LoadInp(gmsh_params,df,nhilos)

    # Create a surface for each inp file
    # to use Contact pair
    N = len(inp_files)
    for i in range(N):
        inp_f = inp_files[i]
        # En este caso tenemos 3 cartas *ELEMENT
        # debido a que el hilo se ha dividido en 3 partes
        # es necesario unirlas en una sola carta *ELEMENT
        element = inp_f.elements[0].merge(inp_f.elements[1])    
        # suponemos que solo hay una carta *ELEMENT
        element = element.merge(inp_f.elements[2])    
        # suponemos que solo hay una carta *ELEMENT
        # eliminamos las cartas *ELEMENT que ya no son necesarias
        # sus elementos se han unido en la primera carta *ELEMENT
        #
        # Recoredemos que el indice 0 es *HEAD y el indice 1 es *NODE
        inp_f.cards = np.delete(inp_f.cards, [2,3,4])
        # insert in 2 position
        inp_f.cards = np.insert(inp_f.cards, 2, element)
        inp_f.reset_cards()

        element = inp_f.elements[0]
        nset    = inp_f.nsets[1]       
         # suponemos que solo hay una carta *NSET
        
        addSurface(inp_files[i],element,nset, "SURFACE_"+str(i+1))
        inp_files[i].SetUniqueNodes()

    # Merge all inp files
    for i in range(1,N):
        inp_files[0].merge(inp_files[i], prefix="P"+str(i+1)+"_")
    # Write the inp file
    file = os.path.join(output_folder,"init.inp")
    inp_files[0].print(file)
    
    nodes = inp_files[0].nodes.df.values
    # homotecia 
    # El radio de la fibra puede verse deformado por los potenciales de lammps 
    # hacemos homotecia para que el radio sea el mismo que el de lammps
    lmp_radius_measure = lmp_params["radius"]
    lmp_target         = lmp_params["r_hebra"]
    params["r_hebra"]  = lmp_target
    nodes = nodes * lmp_target/lmp_radius_measure
    index   = inp_files[0].nodes.df.index
    columns = inp_files[0].nodes.df.columns
    inp_files[0].nodes.df = pd.DataFrame(nodes,
                                         columns=columns,
                                         index  =index)
    #
    #

    # Search the contacts and add the contact pair

    radius = lmp_params["r_hebra"]
    contacts = search_contacts(df,th = 6*radius)
    # save the contacts
    params["contacts"] = contacts
    addStep(inp_files,contacts,file,params)


    name_nsets = [ inset.name     for inset in inp_files[0].nsets]
    data_nsets = [ inset.id_nodes for inset in inp_files[0].nsets]

    nset_dict = dict(zip(name_nsets,data_nsets))

    params["nsets"] = nset_dict
    
    print("Nsets have been created")
    # Save the params
    savejson(params, os.path.join(output_folder,"params.json"))
    # Run the simulation
    error,cmd = runccx(output_folder,
                       name_inp       = "init",
                       att            = params["attemps"],
                       dynamic        = params["calculix_dynamic"],
                       OMP_NUM_THREADS= params["OMP_NUM_THREADS"],
                       mpi            = params["mpi"],
                       mpi_np         = params["mpi_np"])

    params["cmd"] = cmd
    params["frd"] = os.path.join(output_folder,"init.frd")

    # Post process the frd file
    # Calculamos el radio de cada yarn despues de la inflacion
    ComputeRadius(params)

    # Denier
    ComputeDenier(params,nhilos)

    # build new inp file
    CreateDeformedInp(params)
    return params
