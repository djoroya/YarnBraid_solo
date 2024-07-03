import os
from tools.calculix.inp.inp         import inp
import numpy as np
from tools.basic.loadsavejson    import loadjson

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

        
def LoadInp(gmsh_params,df,nhilos):
    # input: gmsh_params, df
    #  - gmsh_params: dict with the path of the inp files
    #  - df: a list of dataframes 
    # =============================================================================
    # Cargamos los paths de los  inp
    # =============================================================================
    folder      = gmsh_params["output_folder"] 
    root_folder = gmsh_params["root_folder"]
    folder      = os.path.join(root_folder,folder)
    # =============================================================================
    #find step files
    files = os.listdir(folder)
    files = [f for f in files if f.endswith('.inp')]
    # 
    #remove 4 last
    files = files[:(8*2*nhilos)]

    # =============================================================================
    # Parseamos los inp
    # =============================================================================
    inp_files = []
    for i in range(len(files)):
        file_name = folder+'/out{}.inp'.format(i+1)
        inp_obj = inp(file_name)
        inp_files.append(inp_obj)

    # =============================================================================
    # Buscamos los puntos centrales  
    # =============================================================================

    # Buscamos los elementos 1D mas cercanos a los puntos centrales

    id_first = []
    for j in range(len(inp_files)):
        lines = [inp_files[j].elements[i] 
                    for i in range(len(inp_files[j].elements)) 
                    if inp_files[j].elements[i].options["TYPE"] == "T3D3"]
        
        min_dist_list = []
        for iline in lines:
            line_points = iline.GetUniqueNodes(inp_files[j].nodes).values
            min_dist = [np.min(np.sum((df[j].values[:, 1:] - iline_points)**2, axis=1))
                        for iline_points in line_points]
            min_dist_list.append(min_dist)

        mean_dist = [np.mean(min_dist) for min_dist in min_dist_list]
        id_sort = np.argsort(mean_dist)
        id_first.append(id_sort[0])

    # Creamos los nsset de los puntos centrales
    cards = [ inp_files[j].FromElement2Nset([id_first[j]],name="esqueleto_"+str(j+1))  
              for j in range(len(inp_files)) ]


    # No estamos interesados en los primeros 2 puntos
    # dado que pertenecen a la cara superior e inferior
    # de manera que los eliminamos

    for j in range(len(inp_files)):
        inp_files[j].nsets[0].id_nodes = inp_files[j].nsets[0].id_nodes[2:]

    # por ultimo eliminamos los elementos 1D
    inp_files = [ inp_files[i].remove_by_type(1) for i in range(len(files))]

    # =============================================================================
    # Agregamos los Nset de la superficie
    # =============================================================================


    id_sort_list = []
    for k,inp_f in enumerate(inp_files):
        surfaces = [inp_f.elements[j] 
                    for j in range(len(inp_f.elements)) 
                    if inp_f.elements[j].options["TYPE"] == "CPS6"]
        
        penalization = [have_first_point(surfaces[i],inp_f,df[k]) for i in range(len(surfaces)) ]
        # from bool to int
        penalization = np.array(penalization).astype(int)

        id_sort = np.argsort([ len(surfaces[i].eid) - 1e3*penalization[i] 
                                for i in range(len(surfaces))])

        id_sort_list.append(id_sort)


    # agregamos Nset de la superficie
    cards = [ inp_files[j].FromElement2Nset(id_sort_list[j][-3:],name="SURF_"+str(j+1))  
            for j in range(len(inp_files)) ]


    # =============================================================================
    # Agregamos los Nset de la cara superior e inferior
    # =============================================================================
    id_sort_list = []

    for inp_f in inp_files:
        surfaces = [inp_f.elements[j]
                    for j in range(len(inp_f.elements))
                    if inp_f.elements[j].options["TYPE"] == "CPS6"]

        id_sort = np.argsort([surfaces[i].GetSTD(inp_f.nodes)
                            for i in range(len(surfaces))])
        surfaces = np.array(surfaces)[id_sort]
        # last
        surfaces = surfaces[:6]

        # GetMassCenter z-value
        MassCenter = [isurf.GetMassCenter(inp_f.nodes)[2] for isurf in surfaces]

        id_sort_mass = np.argsort(MassCenter)
        id_sort = id_sort[id_sort_mass]

        id_sort_list.append(id_sort)


    # Generamos Faces Bot and Top

    for j in range(len(inp_files)):
        inp_files[j].FromElement2Nset(id_sort_list[j][-3:],
                                       name="FACE_TOP_"+str(j+1))
        inp_files[j].FromElement2Nset(id_sort_list[j][:3],
                                       name="FACE_BOT_"+str(j+1))

    # remove elements 2D
    for j in range(len(inp_files)):
        inp_files[j].remove_by_type(2)
    
    for j in range(len(inp_files)):
        for k in range(3):
            inp_files[j].FromElement2Nset([k],"Yarn_"+str(j+1)+"_"+str(k+1))


    # Generamos bot y top de puntos centrales
    #     Card (*NSET) :FACE_TOP_1

    list_name = ["TOP","BOT"]
    id_name  = [2,3]
    for i in range(len(inp_files)):
        for j in range(2):
            i_inp = inp_files[i]
            top_id = i_inp.nsets[id_name[j]].id_nodes
            node_top = i_inp.nodes.df.loc[top_id,:].values
            mean_r = np.mean(node_top,axis=0)
            nearest = np.argmin(np.sum((node_top - mean_r)**2,axis=1))
            top_id = top_id[nearest]
            i_inp.FromId2Nset(np.array([top_id]),
                              name="FACE_"+list_name[j]+\
                                   "_CENTRAL_"+str(i+1))

    return inp_files

