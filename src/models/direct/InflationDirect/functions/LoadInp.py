import os
from tools.calculix.inp.inp         import inp
import numpy as np
from models.direct.InflationDirect.functions.addSurface import addSurface
from settings.simulations import simulations
from tools.basic.loadsavejson import savejson
from models.direct.lammpshard.traj2df import traj2df


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
    #  - df: a list of numpy arrays with shape (n,3)e 
    # =============================================================================
    # Cargamos los paths de los  inp
    # =============================================================================
    folder = os.path.join(simulations() ,gmsh_params["simulation_path"])

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
            traj = df[id_traj].copy()

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
            radius = 0.9*params["lammps_params"]["r_hebra"]*params["gmsh_params"]["factor_radius"]

            bol_near = nodes_rot[:,0]**2 + nodes_rot[:,1]**2 + nodes_rot[:,2]**2 < 4*radius**2

            if ilabel == "BOT":
                bol  = nodes_rot[:,1] < size_mesh/8
            else:
                bol  = nodes_rot[:,1] > -size_mesh/16
            
            bol = np.logical_and(bol,bol_near)

            bot = nodes_rot[bol,:]
            id_bot = id_nodes[bol]

            inp_file.FromId2Nset(id_bot,ilabel+"_"+str(id_traj+1))

            r_mu = np.mean(bot,axis=0)
            dist = np.linalg.norm(bot-r_mu,axis=1)

            id_circ = id_bot[dist>radius]
            inp_file.FromId2Nset(id_circ,"CIRC_"+ilabel+"_"+str(id_traj+1))

            # add nset center of the circle
            try:
                id_nearst = np.argmin(dist)
                id_center = id_bot[id_nearst]
            except:
                
                savejson({"data":nodes_rot,"df":traj2df(df)},"error.json")
                print("Error in LoadInp")
                print("id_traj",id_traj)
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

    id_nset_vols = [ inp_file.elements[i].GetUniqueNodes(inp_file.nodes).index.values
                    for i in range(len(df))]
    
    # inp_file.FromId2Nset 
    for i in range(len(df)):
        inp_file.FromId2Nset(id_nset_vols[i],"YARN_"+str(i+1))


    # =============================================================================
    # creamos nuevos nodos para cada BOT_i pero dezpladaos en z = h/8

    vec = np.array([0,0,params["lammps_params"]["h"]*params["lammps_params"]["len_periodic"]]) # h/8

    # bot_surf_rep = []
    # bot_nset_rep = []
    # for ibot in bot_nset:
    #     label = ibot.name + "_REP"
    #     inset_rep = inp_file.CreateNsetCopy(ibot,label,vec)
    #     inset_rep_s = inp_file.Nset2SurfNode(inset_rep,"SURFACE_"+label)
    #     bot_surf_rep.append(inset_rep_s)
    #     bot_nset_rep.append(inset_rep)
        # inp_file.AddEquation(inset_rep.name,ibot.name)
    # ============================================================================


    # 
    # add new nodes to the inp file 
    # for this 

    all_bonds = params["all_bonds"]

    for bond in all_bonds:
        # top_surface_master = surf_created_top[bond[0]-1]
        # bot_rep_slave      = bot_surf_rep[bond[1]-1]
        # tie_label = "TIE_"+top_surface_master.name+"_"+bot_rep_slave.name
        # inp_file.CreateTie(tie_label,
        #                    slave =bot_rep_slave,
        #                    master=top_surface_master,
        #                    type="surface")
        
        top_nset_master = top_nset[bond[0]-1]
        #bot_nset_slave  = bot_nset_rep[bond[1]-1]
        bot_nset_slave  = bot_nset[bond[1]-1]
        # inp_file.NsetProjection(top_nset_master.name,bot_nset_slave.name)
        # nset1,nset2,type_eq="point2point"
        # inp_file.AddEquation(top_nset_master.name,
        #                      bot_nset_slave.name,
        #                      type_eq="linear_interpolation",dims=[1,2],nodes=inp_file.nodes.df)

    # =============================================================================
    id_mid_inp_list = []
    for w in range(len(df)):
        itraj = df[w]

        len_list = np.sqrt(np.sum(np.diff(itraj,axis=0)**2,axis=1))
        cdist = np.cumsum(len_list)

        cmid = cdist[-1]/2

        ind_mid = np.argmin(np.abs(cdist-cmid))

        mid_point = itraj[ind_mid]

        # find id in inp_file.nodes.df
        id_inp = inp_file.nodes.df.index.values
        nodes = inp_file.elements[w].GetUniqueNodes(inp_file.nodes)
        id_inp = nodes.index.values

        distances = np.sum((mid_point - nodes)**2,axis=1)
        id_mid_inp = id_inp[np.argmin(distances)]
        inp_file.FromId2Nset([id_mid_inp],"MID_POINT_"+str(w+1))

        id_mid_inp_list.append(id_mid_inp)
        # create a nset with the mid point
    inp_file.FromId2Nset(id_mid_inp_list,"MID_POINTS")



    return inp_file

