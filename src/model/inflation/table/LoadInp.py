import os
from tools.calculix.inp.inp         import inp
import numpy as np
from model.inflation.table.addSurface import addSurface
import pandas as pd

def have_first_point(isurf,inp_f,df):
    # dado una superficie isurf, un inp inp_f y un df

    r0           = df.iloc[0,1:].values
    matrix_nodes = inp_f.nodes.df.iloc[:,:].values

    distances = np.sum((r0 - matrix_nodes)**2,axis=1)

    index = np.arange(1,inp_f.nodes.df.shape[0]+1)
    index = index[distances < 1e-2]


    surf_nids = isurf.GetUniqueNodes(inp_f.nodes).index.values

    inside = False
    for ii in index:
        if ii in surf_nids:
            inside = True
            break

    return inside

        
def LoadInp(gmsh_params,df,params):
    # input: gmsh_params, df
    #  - gmsh_params: dict with the path of the inp files
    #  - df: a list of dataframes 
    # =============================================================================
    # Cargamos los paths de los  inp
    # =============================================================================
    folder = os.path.join(gmsh_params["root_folder"] ,gmsh_params["output_folder"])

    #find step files
    files = os.listdir(folder)
    files = [f for f in files if f.endswith('.inp')]
    # =============================================================================
    # Parseamos los inp
    # =============================================================================
    inp_file = inp(os.path.join(folder,files[0]),warning=True)


    # =============================================================================
    surfaces = [ el for el in inp_file.elements 
                if el.options["TYPE"] == "CPS6"]

    for j in range(len(df)):
        nodes = surfaces[j].GetUniqueNodes(inp_file.nodes)
        nid_groups = nodes.index.values
        inp_file.FromId2Nset(nid_groups,"SURFACE_PRE_"+str(j+1))
    inp_file.remove_by_type(2) 

    # Agregar BOT y TOP
    id_traj = 0
    for ilabel in ["BOT","TOP"]:
        for id_traj in range(len(df)):
            nodes    = inp_file.elements[id_traj].GetUniqueNodes(inp_file.nodes)
            id_nodes = nodes.index.values.copy()
            nodes = nodes.values.copy()
            traj = df[id_traj][["x","y","z"]].values.copy()

            # cambio de variable a los nodos 
            # para que esten descritos en el sistema de coordenadas
            # en el que el primer punto de la trayectoria es el origen
            # y el eje z es la direccion de la trayectoria

            if ilabel == "BOT":
                r0 = traj[0,:]
                vy = traj[1,:]-traj[0,:]
            else:
                r0 = traj[-1,:]
                vy = traj[-1,:]-traj[-2,:]
                
            vy = vy/np.linalg.norm(vy)
            # 
            # seed 
            np.random.seed(0)
            v_rand = np.random.rand(3)
            v_rand = v_rand/np.linalg.norm(v_rand)
            #
            vx = np.cross(vy,v_rand)
            vx = vx/np.linalg.norm(vx)
            #
            vz = np.cross(vx,vy)
            vz = vz/np.linalg.norm(vz)
            #
            R = np.array([vx,vy,vz])

            #
            nodes_rot = np.dot(nodes - r0,R.T) 

            size_mesh = gmsh_params["MeshSizeMin"]
            if ilabel == "BOT":
                bol  = nodes_rot[:,1] < size_mesh/8
            else:
                bol  = nodes_rot[:,1] > -size_mesh/8
            bot = nodes_rot[bol,:]
            id_bot = id_nodes[bol]

            inp_file.FromId2Nset(id_bot,ilabel+"_"+str(id_traj+1))

            r_mu = np.mean(bot,axis=0)
            dist = np.linalg.norm(bot-r_mu,axis=1)
            radius = 0.9*params["lammps_params"]["r_hebra"]*params["gmsh_params"]["factor_radius"]

            id_circ = id_bot[dist>radius]
            inp_file.FromId2Nset(id_circ,"CIRC_"+ilabel+"_"+str(id_traj+1))

            # add nset center of the circle
            id_nearst = np.argmin(dist)
            id_center = id_bot[id_nearst]
            #from nodes 

            inp_file.FromId2Nset([id_center],
                                 "PCIRC_"+ilabel+"_"+str(id_traj+1)+"_CENTER")

    bot_nset      = [nset for nset in inp_file.nsets 
                     if "BOT" == nset.name[:3]]
    
    top_nset      = [nset for nset in inp_file.nsets 
                     if "TOP" == nset.name[:3]]
    
    circ_top_nset = [nset for nset in inp_file.nsets 
                     if "CIRC_TOP" == nset.name[:8]]
    
    circ_bot_nset = [nset for nset in inp_file.nsets 
                     if "CIRC_BOT" == nset.name[:8]]
    
    surf_nset     = [nset for nset in inp_file.nsets 
                     if "SURFACE" in nset.name]

    # Comprobamos que no existe de los tapas en el esqueleto
    # si existe, lo eliminamos
    esq_nset = [nset for nset in inp_file.nsets
                if "ESQUELETO" in nset.name]
    tapas = list()
    tapas.extend(bot_nset)
    tapas.extend(top_nset)
    
    for iesq in esq_nset:
        for itapa in tapas:
            iesq.id_nodes = np.setdiff1d( iesq.id_nodes,
                                         itapa.id_nodes)
    # Creamos *SURFACE para cada superficie
    # y agregamos los nsets de cada superficie
    for i in range(len(df)):
        bot_id      = bot_nset[i]
        top_id      = top_nset[i]
        circ_bot_id = circ_bot_nset[i]
        circ_top_id = circ_top_nset[i]
        sur_id      = surf_nset[i]

        tapas   = np.concatenate((bot_id.id_nodes,top_id.id_nodes)) 
        circ_id = np.concatenate((circ_bot_id.id_nodes,circ_top_id.id_nodes))
        sur_id  = sur_id.id_nodes
        #
        sur_id_new = np.setdiff1d(sur_id,tapas)
        sur_id_new = np.concatenate((sur_id_new,circ_id))
        #
        inp_file.FromId2Nset(sur_id_new,"SURFACE_"+str(i+1))

    surf_nset = [nset for nset in inp_file.nsets 
                        if "SURFACE" in nset.name][len(df):]

    addSurface(inp_file,"SURFACE",surf_nset)
    surf_created_top = addSurface(inp_file,"TOP",top_nset)
    surf_created_bot = addSurface(inp_file,"BOT",bot_nset)


    # sel_df_top = lambda id_traj: df[id_traj].iloc[-1,1:].values
    # sel_df_bot = lambda id_traj: df[id_traj].iloc[0 ,1:].values
    

    
    # vec_list = [    sel_df_top(3) - sel_df_bot(0) ,
    #                 sel_df_top(1) - sel_df_bot(2) ,
    #                 sel_df_top(0) - sel_df_bot(3),
    #                 sel_df_top(2) - sel_df_bot(1)
    #                 ]
    
    # rep_nset_list = [bot_nset[0],
    #                  bot_nset[2],
    #                  bot_nset[3],
    #                  bot_nset[1]
    #                   ]
    
    # label_list     = ["BOT_1_rep",
    #                   "BOT_3_rep",
    #                   "BOT_4_rep",
    #                   "BOT_2_rep"
    #                   ]
    
    # glue_surf = [
    #     surf_created_top[3],
    #     surf_created_top[1],
    #     surf_created_top[0],
    #     surf_created_top[2]
    # ]

    # for k in range(4):
    #     vec      = vec_list[k]
    #     rep_nset = rep_nset_list[k]
    #     label    = label_list[k]
    #     glu      = glue_surf[k]

    #     # create a nset with the new nodes
    #     inset_rep = inp_file.CreateNsetCopy(rep_nset,label,vec)
    #     # create a surface with the new nodes
    #     node_surf = inp_file.Nset2SurfNode(inset_rep,"SURFACE_"+label)

    #     inp_file.CreateTie("TIE_"+label,
    #                        slave =node_surf.name,
    #                        master=glu.name)

    #     inp_file.AddEquation(rep_nset.name,inset_rep.name)

    return inp_file

